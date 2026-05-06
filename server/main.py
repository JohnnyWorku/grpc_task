import grpc
import time
from concurrent import futures
import inference_pb2
import inference_pb2_grpc

class AIInferenceService(inference_pb2_grpc.AIInferenceServicer):
    
    def AnalyzeSentiment(self, request, context):
        return inference_pb2.SentimentResponse(label="POSITIVE", confidence=0.98)

    def StreamChat(self, request, context):
        response_text = f"AI Response to: {request.prompt}"
        for word in response_text.split():
            yield inference_pb2.TokenResponse(token=word + " ")
            time.sleep(0.2)

    def SummarizeDocument(self, request_iterator, context):
        full_text = "".join([chunk.text for chunk in request_iterator])
        return inference_pb2.SummaryResponse(summary=f"Summary of {len(full_text)} chars.")

    def LiveAssistant(self, request_iterator, context):
        for msg in request_iterator:
            yield inference_pb2.ChatMessage(role="assistant", content=f"Echo: {msg.content}")

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    inference_pb2_grpc.add_AIInferenceServicer_to_server(AIInferenceService(), server)
    server.add_insecure_port('[::]:50051')
    print("Server started on port 50051")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()