# AI Inference Microservice Mesh

This project is a high-performance, horizontally scalable AI Inference Microservice built using **gRPC** and **Python**. It integrates **Gemini 2.0 Flash** for real-time AI generation and utilizes **Nginx** as a Layer 7 Load Balancer to distribute traffic across a containerized mesh of inference servers.

---

## Architecture Overview

In modern backend engineering, LLMs require persistent, low-latency connections. This project solves that by using:

* **gRPC & Protobuf:** Strict API contracts and binary serialization for high-speed data transfer.
* **HTTP/2:** Native support for multiplexing and long-lived bidirectional streams.
* **Layer 7 Load Balancing:** Nginx is configured as a gRPC reverse proxy to balance requests at the RPC level, ensuring efficient resource utilization across replicas.

---

## Technology Stack

* **RPC Framework:** gRPC & Protocol Buffers (Protobuf)
* **Language:** Python 3.10+
* **AI Engine:** Google Gemini 2.0 Flash (via `google-genai` SDK)
* **Infrastructure:** Docker & Docker Compose
* **Load Balancer:** Nginx (configured for HTTP/2 and `grpc_pass`)

---

## Project Structure

```text
.
├── protos/             # Protocol Buffer (.proto) definitions
├── server/             # Backend logic & Gemini 2.0 integration
├── client/             # CLI Tester script & generated stubs
├── nginx/              # Nginx L7 Load Balancer configuration
├── docker-compose.yml  # Orchestration of the 3-server mesh
├── Makefile            # Automation for code generation
└── README.md           # Documentation


# Setup and Execution (Step-by-Step)

## 1. Prerequisites

Ensure you have the following installed on your host machine:

- Docker & Docker Compose  
- Python 3.10 or higher  
- Make (optional, for automation)

---

## 2. Prepare the Workspace

Open your terminal in the project root folder and execute the following:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment

# Linux/macOS:
source venv/bin/activate

# Windows:
# .\venv\Scripts\activate

# Install the necessary compiler libraries and SDK
pip install grpcio-tools protobuf google-genai


## 3. API Key Integration


Navigate to Google AI Studio and generate an API Key.


Open server/main.py.


Locate the line:


client = genai.Client(api_key="YOUR_ACTUAL_API_KEY_HERE")


Paste your API key inside the quotes.



## 4. Compile the Protobuf Files
You must generate the Python gRPC stubs before building the Docker containers.
This creates the communication bridge between the client and the servers.
# Option A: Using the Makefilemake gen_proto# Option B: Manual Commandpython3 -m grpc_tools.protoc -I./protos --python_out=server/ --grpc_python_out=server/ protos/inference.protopython3 -m grpc_tools.protoc -I./protos --python_out=client/ --grpc_python_out=client/ protos/inference.proto

## 5. Build and Launch the Mesh
Start the containerized environment. This will spin up three AI servers and one Nginx load balancer:
# Clean up any existing containers or orphaned networksdocker compose down# Build the images from the Dockerfile and start the servicesdocker compose up --build

## 6. Run the Test Client
Open a new terminal window, navigate to the project root directory, and run:
# Activate venv again in this new terminal sessionsource venv/bin/activate# Execute the tester script to perform all 4 gRPC taskspython client/tester.py
