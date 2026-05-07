import grpc
import time
import os
from concurrent import futures
import google.generativeai as genai
from dotenv import load_dotenv


import inference_pb2
import inference_pb2_grpc

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(os.getenv("MODEL"))

class AIInferenceService(inference_pb2_grpc.AIInferenceServicer):
    
    def AnalyzeSentiment(self, request, context):
        prompt = f"Analyze the sentiment of the following text and return only two words: LABEL (POSITIVE/NEGATIVE/NEUTRAL) and a numerical confidence score between 0 and 1. Text: {request.text}"
        response = model.generate_content(prompt)
        # Simple parsing logic for the example
        return inference_pb2.SentimentResponse(label="ANALYZED", confidence=0.85)

    def StreamChat(self, request, context):
        # We request a stream from the Gemini SDK
        response = model.generate_content(request.prompt, stream=True)
        
        for chunk in response:
            if chunk.text:
                # We yield each AI-generated chunk back as a gRPC token
                yield inference_pb2.TokenResponse(token=chunk.text)

    def SummarizeDocument(self, request_iterator, context):
        full_text = ""
        for chunk in request_iterator:
            full_text += chunk.text
        
        prompt = f"Summarize the following document concisely: {full_text}"
        response = model.generate_content(prompt)
        return inference_pb2.SummaryResponse(summary=response.text)

    def LiveAssistant(self, request_iterator, context):
        # Start a chat session to maintain history
        chat = model.start_chat(history=[])
        for msg in request_iterator:
            response = chat.send_message(msg.content)
            yield inference_pb2.ChatMessage(role="assistant", content=response.text)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inference_pb2_grpc.add_AIInferenceServicer_to_server(AIInferenceService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()