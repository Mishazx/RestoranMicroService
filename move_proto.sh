mkdir -p ./OrderService/pb2
mkdir -p ./WebService/pb2
mkdir -p ./KitchenService/pb2
mkdir -p ./NotificationService/pb2

cp ./protoc/pb2/order_pb2.py ./OrderService/pb2
cp ./protoc/pb2/order_pb2_grpc.py ./OrderService/pb2

cp ./protoc/pb2/kitchen_pb2.py ./OrderService/pb2
cp ./protoc/pb2/kitchen_pb2_grpc.py ./OrderService/pb2

cp ./protoc/pb2/notification_pb2.py ./OrderService/pb2
cp ./protoc/pb2/notification_pb2_grpc.py ./OrderService/pb2

cp ./protoc/pb2/order_pb2.py ./WebService/pb2
cp ./protoc/pb2/order_pb2_grpc.py ./WebService/pb2

cp ./protoc/pb2/kitchen_pb2.py ./KitchenService/pb2
cp ./protoc/pb2/kitchen_pb2_grpc.py ./KitchenService/pb2

cp ./protoc/pb2/order_pb2.py ./KitchenService/pb2
cp ./protoc/pb2/order_pb2_grpc.py ./KitchenService/pb2

cp ./protoc/pb2/notification_pb2.py ./NotificationService/pb2
cp ./protoc/pb2/notification_pb2_grpc.py ./NotificationService/pb2

# cp ./proto/pb2/notification_pb2.py ./KitchenService/pb2
# cp ./proto/pb2/notification_pb2_grpc.py ./KitchenService/pb2

# cp ./proto/kitchen_pb2.py ./WebService/pb2
# cp ./proto/kitchen_pb2_grpc.py ./WebService/pb2

# cp ./proto/notification_pb2.py ./WebService/pb2
# cp ./proto/notification_pb2_grpc.py ./WebService/pb2

