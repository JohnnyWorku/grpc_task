import logging

import grpc
import time
import os
from concurrent import futures
import google.generativeai as genai
from groq import Groq
from dotenv import load_dotenv


import inference_pb2
import inference_pb2_grpc

load_dotenv()

# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
model = os.getenv("GROQ_MODEL")

class AIInferenceService(inference_pb2_grpc.AIInferenceServicer):
    
    def AnalyzeSentiment(self, request, context):
        prompt = f"Analyze the sentiment of the following text and return only two words: its LABEL (eg: POSITIVE/NEGATIVE/NEUTRAL) and a numerical confidence score between 0 and 1. Text: {request.text}"
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        ai_text = response.choices[0].message.content
        
        return inference_pb2.SentimentResponse(response=ai_text)

    def StreamChat(self, request, context):
        
        stream = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": request.prompt}
            ],
            stream=True
        )
        
        for chunk in stream:
            content = chunk.choices[0].delta.content
            
            if content:
                yield inference_pb2.TokenResponse(token=content)

    def SummarizeDocument(self, request_iterator, context):
        file_data = bytearray()
        file_name = ""
        
        for request in request_iterator:
            if request.info.file_name:
                file_name = request.info.file_name
                logging.info(f"Receiving file: {file_name}")

            elif request.chunk_data:
                file_data.extend(request.chunk_data)
                logging.info(f"Got chunk size: {len(request.chunk_data)}")
        
        
        if not file_data:
            return inference_pb2.UploadFileResponse(summary="Error: No data")
            
        logging.info(f"Total bytes received: {len(file_data)}")
        

        text = file_data.decode("utf-8", errors="ignore")

        prompt = f"""
        Summarize the following file content concisely:

        {text}
        """

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        summary = response.choices[0].message.content

        return inference_pb2.UploadFileResponse(summary=summary)

    def LiveAssistant(self, request_iterator, context):
        history = []

        for msg in request_iterator:
            history.append({"role": "user", "content": msg.content})

            stream = client.chat.completions.create(
                model=model,
                messages=history,
                stream=True
            )

            assistant_message = ""

            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    assistant_message += content
                    yield inference_pb2.ChatMessage(
                        role="assistant",
                        content=content
                    )

            # save assistant response to history
            history.append({"role": "assistant", "content": assistant_message})

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inference_pb2_grpc.add_AIInferenceServicer_to_server(AIInferenceService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()