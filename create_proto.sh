# python3 -m grpc_tools.protoc -I./proto/files --python_out=./proto --grpc_python_out=./proto ./proto/files/order.proto 

# python3 -m grpc_tools.protoc -I./proto/files --proto_path=./proto/files --python_out=./proto --grpc_python_out=./proto ./proto/files/order.proto

python3 -m grpc_tools.protoc -I./protoc/files --python_out=./protoc/pb2 --grpc_python_out=./protoc/pb2 ./protoc/files/order.proto

python3 -m grpc_tools.protoc -I./protoc/files --python_out=./protoc/pb2 --grpc_python_out=./protoc/pb2 ./protoc/files/kitchen.proto

python3 -m grpc_tools.protoc -I./protoc/files --python_out=./protoc/pb2 --grpc_python_out=./protoc/pb2 ./protoc/files/notification.proto