FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем только proto файлы
# COPY proto/order.proto proto/
# COPY protos/kitchen.proto protos/
# COPY protos/notification.proto protos/

# # Генерируем Python код из proto файлов
# RUN python -m grpc_tools.protoc \
#     -I./proto \
#     --python_out=. \
#     --grpc_python_out=. \
#     protos/order.proto \
    # protos/kitchen.proto \
    # protos/notification.proto

# Копируем остальной код
COPY . .

CMD ["python", "OrderServer.py"] 