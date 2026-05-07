PROTO_SRC=protos/inference.proto
SERVER_OUT=server/
CLIENT_OUT=client/


gen_proto:
	python3 -m grpc_tools.protoc -I./protos --python_out=$(SERVER_OUT) --grpc_python_out=$(SERVER_OUT) $(PROTO_SRC)
	python3 -m grpc_tools.protoc -I./protos --python_out=$(CLIENT_OUT) --grpc_python_out=$(CLIENT_OUT) $(PROTO_SRC)


build:
	sudo docker compose build --no-cache

up:
	sudo docker compose up --build

down:
	sudo docker compose down

client_tester:
	python3 client/tester.py
