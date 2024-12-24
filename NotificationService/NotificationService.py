import grpc
from concurrent import futures
import logging
from datetime import datetime
import asyncio
from threading import Thread

import pb2.notification_pb2 as notification_pb2
import pb2.notification_pb2_grpc as notification_pb2_grpc
from database import init_db, SessionLocal, Notification
from db_check import wait_for_db
from WebSocketServer import app, notification_manager
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('NotificationService')

class NotificationService(notification_pb2_grpc.NotificationServiceServicer):
    def NotifyOrderStatus(self, request, context):
        logger.info(f"Received notification request for order {request.order_id}")
        
        try:
            # Создаем сессию базы данных
            db = SessionLocal()
            
            # Создаем новую запись уведомления
            notification = Notification(
                order_id=request.order_id,
                table_number=request.table_number,
                status=request.status,
                message=request.message
            )
            
            # Сохраняем в базу данных
            db.add(notification)
            db.commit()
            
            logger.info(f"Notification saved to database: Order {request.order_id}, Status: {request.status}")
            
            # Закрываем сессию
            db.close()

            # Отправляем уведомление через WebSocket
            notification_data = {
                "order_id": request.order_id,
                "table_number": request.table_number,
                "status": request.status,
                "message": request.message,
                "timestamp": datetime.now().isoformat()
            }
            
            asyncio.run(notification_manager.broadcast(notification_data))
            
            return notification_pb2.NotificationResponse(
                success=True,
                message="Notification processed successfully"
            )
            
        except Exception as e:
            logger.error(f"Error processing notification: {str(e)}")
            return notification_pb2.NotificationResponse(
                success=False,
                message=f"Error processing notification: {str(e)}"
            )

def run_grpc_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    notification_pb2_grpc.add_NotificationServiceServicer_to_server(
        NotificationService(), server
    )
    server.add_insecure_port('[::]:50053')
    server.start()
    logger.info("gRPC Notification Service is running on port 50053")
    server.wait_for_termination()

def run_websocket_server():
    uvicorn.run(app, host="0.0.0.0", port=8080)

def serve():
    # Ждем готовности базы данных
    logger.info("Waiting for database to be ready...")
    wait_for_db()
    
    # Инициализируем базу данных
    init_db()
    logger.info("Database initialized")
    
    # Запускаем gRPC и WebSocket серверы в разных потоках
    grpc_thread = Thread(target=run_grpc_server)
    websocket_thread = Thread(target=run_websocket_server)
    
    grpc_thread.start()
    websocket_thread.start()
    
    grpc_thread.join()
    websocket_thread.join()

if __name__ == '__main__':
    serve() 