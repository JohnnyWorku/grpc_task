# AI Inference Microservice Mesh

This project is a high-performance, horizontally scalable AI Inference Microservice built using **gRPC** and **Python**. It integrates **Gemini** for real-time AI generation and utilizes **Nginx** for Layer 7 load balancing.

---

## Architecture Overview

In modern backend engineering, LLMs require persistent, low-latency connections. This project addresses that by using:

- **gRPC & Protobuf:** Strict API contracts and binary serialization for high-speed data transfer.
- **HTTP/2:** Native support for multiplexing and long-lived bidirectional streams.
- **Layer 7 Load Balancing:** Nginx is configured as a gRPC reverse proxy to balance requests at the RPC level, ensuring efficient resource utilization across replicas.

---

## Technology Stack

- **RPC Framework:** gRPC & Protocol Buffers (Protobuf)
- **Language:** Python 3.10+
- **AI Engine:** Google Gemini 2.0 Flash (via `google-genai` SDK)
- **Infrastructure:** Docker & Docker Compose
- **Load Balancer:** Nginx (configured for HTTP/2 and `grpc_pass`)

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
```

---

## Setup and Execution

### 1. Prerequisites

Ensure you have the following installed on your host machine:

- Docker & Docker Compose  
- Python 3.10 or higher  
- Make (optional, for automation)

---

### 2. Prepare the Workspace

Open your terminal in the project root folder and execute:

```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
# For Linux/macOS:
source venv/bin/activate

# For Windows:
# .\venv\Scripts\activate

# Install the necessary compiler libraries and SDK
pip install grpcio-tools protobuf google-genai
```

---

### 3. API Key Integration

- Generate an API Key from [Google AI Studio](https://aistudio.google.com/).
- Open `server/main.py`.
- Locate the following line:

  ```python
  client = genai.Client(api_key="YOUR_ACTUAL_API_KEY_HERE")
  ```

- Paste your API key inside the quotes or create .env file and use the original code same way.

---

### 4. Compile the Protobuf Files

You must generate the Python gRPC stubs before building the Docker containers. This step creates the communication bridge between the client and the server.

- **Option A: Using the Makefile**

  ```bash
  make gen_proto
  ```

- **Option B: Manual Command**

  ```bash
  python3 -m grpc_tools.protoc -I./protos \
    --python_out=server/ --grpc_python_out=server/ \
    protos/inference.proto
  ```

---

### 5. Build and Launch the Mesh

Start the containerized environment. This will spin up three AI servers and one Nginx load balancer.

```bash
# Using Makefile
make down

# Clean up any existing containers or orphaned networks -- manually
docker compose down

# Using Makefile
make up

# Build the images from the Dockerfile and start the services -- manually
docker compose up --build
```

---

### 6. Run the Test Client

Open a new terminal window, navigate to the project root directory, and run:

```bash
# Activate venv again in this new terminal session
source venv/bin/activate

# Execute the tester script to perform all 4 gRPC tasks
python client/tester.py
```

---

## Output Examples

Below are example outputs from running the test client against the microservice mesh:

### Test Run 1
![Output 1](https://github.com/JohnnyWorku/grpc_task/raw/main/images/image_1.png)

![Output 2](https://github.com/JohnnyWorku/grpc_task/raw/main/images/image_2.png)
