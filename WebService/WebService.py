from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import grpc
import pb2.order_pb2 as order_pb2
import pb2.order_pb2_grpc as order_pb2_grpc
import logging
from datetime import datetime
from enum import Enum

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('WebService')

app = FastAPI(title="Restaurant Web Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # Разрешаем запросы с React приложения
    allow_credentials=True,
    allow_methods=["*"],  # Разрешаем все методы (GET, POST, etc.)
    allow_headers=["*"],  # Разрешаем все заголовки
)

# Определяем enum для статусов заказа
class OrderStatus(str, Enum):
    PENDING = "PENDING"
    COOKING = "COOKING"
    READY = "READY"
    DELIVERED = "DELIVERED"
    PICKED_UP = "PICKED_UP"
    CANCELLED = "CANCELLED"

# Модели Pydantic для валидации данных
class MenuItem(BaseModel):
    id: int
    name: str
    quantity: int

class CreateOrderRequest(BaseModel):
    table_number: int
    items: List[MenuItem]

class OrderResponse(BaseModel):
    id: str
    table_number: int
    items: List[MenuItem]
    status: OrderStatus
    created_at: str

# gRPC клиент
class OrderServiceClient:
    def __init__(self):
        self.channel = grpc.insecure_channel('order_service:50051')
        self.stub = order_pb2_grpc.OrderServiceStub(self.channel)

    def create_order(self, request: CreateOrderRequest) -> OrderResponse:
        try:
            items = [
                order_pb2.MenuItem(
                    id=item.id,
                    name=item.name,
                    quantity=item.quantity
                ) for item in request.items
            ]
            
            grpc_request = order_pb2.CreateOrderRequest(
                table_number=request.table_number,
                items=items
            )
            
            response = self.stub.CreateOrder(grpc_request)
            return OrderResponse(
                id=response.order_id,
                table_number=response.table_number,
                items=[MenuItem(
                    id=item.id,
                    name=item.name,
                    quantity=item.quantity
                ) for item in response.items],
                status=OrderStatus(order_pb2.OrderStatus.Name(response.status)),  # Конвертируем enum в строку
                created_at=response.created_at
            )
        except grpc.RpcError as e:
            logger.error(f"gRPC error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"gRPC error: {str(e)}")

    def get_order(self, id: str) -> OrderResponse:
        try:
            response = self.stub.GetOrder(
                order_pb2.GetOrderRequest(order_id=id)
            )
            return OrderResponse(
                id=response.order_id,
                table_number=response.table_number,
                items=[MenuItem(
                    id=item.id,
                    name=item.name,
                    quantity=item.quantity
                ) for item in response.items],
                status=OrderStatus(order_pb2.OrderStatus.Name(response.status)),  # Конвертируем enum в строку
                created_at=response.created_at
            )
        except grpc.RpcError as e:
            logger.error(f"gRPC error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"gRPC error: {str(e)}")

    def update_order_status(self, id: int, status: str) -> OrderResponse:
        try:
            grpc_status = order_pb2.OrderStatus.Value(status)
            response = self.stub.UpdateOrderStatus(
                order_pb2.UpdateOrderStatusRequest(order_id=id, status=grpc_status)
            )
            return OrderResponse(
                order_id=response.id,
                table_number=response.table_number,
                items=[MenuItem(
                    id=item.id,
                    name=item.name,
                    quantity=item.quantity
                ) for item in response.items],
                status=OrderStatus(order_pb2.OrderStatus.Name(response.status)),
                created_at=response.created_at
            )
        except grpc.RpcError as e:
            logger.error(f"gRPC error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"gRPC error: {str(e)}")

    def confirm_order_pickup(self, id: str) -> OrderResponse:
        try:
            response = self.stub.ConfirmOrderPickup(
                order_pb2.ConfirmOrderPickupRequest(order_id=id)
            )
            return OrderResponse(
                id=response.order_id,
                table_number=response.table_number,
                items=[MenuItem(
                    id=item.id,
                    name=item.name,
                    quantity=item.quantity
                ) for item in response.items],
                status=OrderStatus(order_pb2.OrderStatus.Name(response.status)),
                created_at=response.created_at
            )
        except grpc.RpcError as e:
            logger.error(f"gRPC error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"gRPC error: {str(e)}")


order_client = OrderServiceClient()

@app.post("/orders/", response_model=OrderResponse)
async def create_order(request: CreateOrderRequest):
    """Create a new order"""
    return order_client.create_order(request)

@app.get("/orders/{id}", response_model=OrderResponse)
async def get_order(id: str):
    """Get order status by ID"""
    return order_client.get_order(id)

@app.put("/orders/{id}/confirm-pickup", response_model=OrderResponse)
async def confirm_order_pickup(id: str):
    """Confirm order pickup by ID"""
    return order_client.confirm_order_pickup(id)