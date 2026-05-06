import grpc
import time
import sys
import os

# Ensure the generated proto files are in the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import inference_pb2
import inference_pb2_grpc

def run_tests():
    # Connect to the Nginx Load Balancer port (8080)
    # Nginx will then route this to one of the 3 backend servers
    channel = grpc.insecure_channel('localhost:8080')
    stub = inference_pb2_grpc.AIInferenceStub(channel)

    print("--- Task 2: Unary (Sentiment Analysis) ---")
    try:
        # We set a 2.0s deadline as per bonus requirements
        request = inference_pb2.SentimentRequest(text="This gRPC microservice is incredibly fast!")
        response = stub.AnalyzeSentiment(request, timeout=2.0)
        print(f"Result: {response.label} | Confidence: {response.confidence}")
    except grpc.RpcError as e:
        print(f"Unary failed: {e.code()} - {e.details()}")

    print("\n--- Task 3: Server Streaming (Chat Generation) ---")
    prompt = inference_pb2.PromptRequest(prompt="Write a 1-sentence story.")
    for token_resp in stub.StreamChat(prompt):
        print(f"{token_resp.token}", end="", flush=True)
    print("\n")

    print("--- Task 4: Client Streaming (Batch Summarization) ---")
    def generate_chunks():
        messages = ["Chunk 1: AI is evolving. ", "Chunk 2: gRPC is efficient. ", "Chunk 3: Scale is key."]
        for msg in messages:
            yield inference_pb2.DocumentChunk(text=msg)
    
    summary = stub.SummarizeDocument(generate_chunks())
    print(f"Final Summary: {summary.summary}")

    print("\n--- Task 5: Bidirectional Streaming (Live Chat) ---")
    def chat_it():
        for i in range(3):
            msg = f"Message {i+1}"
            print(f"Sending: {msg}")
            yield inference_pb2.ChatMessage(role="user", content=msg)
            time.sleep(0.5)

    responses = stub.LiveAssistant(chat_it())
    for resp in responses:
        print(f"AI Response: {resp.content}")

if __name__ == '__main__':
    run_tests()