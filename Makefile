PROTO_SRC=protos/inference.proto
SERVER_OUT=server/
CLIENT_OUT=client/


gen_proto:
	python3 -m grpc_tools.protoc -I./protos --python_out=$(SERVER_OUT) --grpc_python_out=$(SERVER_OUT) $(PROTO_SRC)
	python3 -m grpc_tools.protoc -I./protos --python_out=$(CLIENT_OUT) --grpc_python_out=$(CLIENT_OUT) $(PROTO_SRC)


build:
	docker compose build

up:
	docker compose up

down:
	docker compose down
