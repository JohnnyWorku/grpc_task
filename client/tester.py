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

    print("--- Unary (Sentiment Analysis) ---")
    try:
        user_input = input("Enter your sentence for sentiment analysis: ")
        request = inference_pb2.SentimentRequest(text=user_input)
        response = stub.AnalyzeSentiment(request)
        print(response)
    except grpc.RpcError as e:
        print(f"Unary failed: {e.code()} - {e.details()}")

    print("\n--- Server Streaming (Chat Generation) ---")
    user_request = input("Ask any question like(eg: tell me a story or tell me a joke): ")
    prompt = inference_pb2.PromptRequest(prompt=user_request)
    print("\n")
    for token_resp in stub.StreamChat(prompt):
        print(f"{token_resp.token}", end="", flush=True)
    print("\n")

    print("--- Client Streaming (Batch Summarization) ---")
    def generate_chunks(file_path, chunk_size=64 * 1024):
        file_name = os.path.basename(file_path)
        file_type = os.path.splitext(file_path)[1]

        metadata = inference_pb2.FileInfo(
            file_name=file_name,
            file_type=file_type
        )
        
        yield inference_pb2.UploadFileRequest(info=metadata)

        # stream file
        with open(file_path, "rb") as f:
            while True:
                chunk = f.read(chunk_size)
                if not chunk:
                    break

                yield inference_pb2.UploadFileRequest(chunk_data=chunk)
    
    def summarize_document(stub, file_path):
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found.")
            return
        
        iterator_request = generate_chunks(file_path)
        
        try:
            response = stub.SummarizeDocument(iterator_request)
            print("\n Summary:\n")
            print(response.summary)

        except grpc.RpcError as e:
            print(f"Error: {e.code()} - {e.details()}")
            
    user_file_path_input = input("Enter the file path to summarize: ")
    summarize_document(stub, user_file_path_input)

    print("\n--- Bidirectional Streaming (Live Chat) ---")
    
    while True:
        user_input = input("You: ")
        
        if user_input.lower() in ["exit", "quit", "stop"]:
            print("Good bye!")
            break
    
        def live_chat():
            yield inference_pb2.ChatMessage(role="user", content=user_input)

        responses = stub.LiveAssistant(live_chat())
        
        print(f"AI Response: ", end="", flush=True)
        
        for resp in responses:
            print(resp.content, end="", flush=True)

        print("\n")
        

if __name__ == '__main__':
    run_tests()