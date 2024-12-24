import grpc
from concurrent import futures
import logging
import time
import random
from datetime import datetime

import pb2.kitchen_pb2 as kitchen_pb2
import pb2.kitchen_pb2_grpc as kitchen_pb2_grpc
import pb2.order_pb2 as order_pb2
import pb2.order_pb2_grpc as order_pb2_grpc

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('KitchenService')

class KitchenService(kitchen_pb2_grpc.KitchenServiceServicer):
    def __init__(self):
        self.order_channel = grpc.insecure_channel('order_service:50051')
        self.order_stub = order_pb2_grpc.OrderServiceStub(self.order_channel)
        logger.info("Kitchen Service initialized")

    def ProcessOrder(self, request, context):
        logger.info(f"Received order to process: {request.order_id}")
        
        # Симулируем время приготовления
        estimated_time = random.randint(5, 15)
        logger.info(f"Estimated cooking time for order {request.order_id}: {estimated_time} minutes")
        
        # Запускаем асинхронное приготовление
        def cook_order():
            time.sleep(estimated_time)  # Симулируем приготовление
            try:
                # Обновляем статус заказа на READY
                update_request = order_pb2.UpdateOrderStatusRequest(
                    order_id=request.order_id,
                    status=order_pb2.OrderStatus.READY
                )
                self.order_stub.UpdateOrderStatus(update_request)
                logger.info(f"Order {request.order_id} is ready")
            except grpc.RpcError as e:
                logger.error(f"Failed to update order status: {str(e)}")
        
        # Запускаем приготовление в отдельном потоке
        from threading import Thread
        Thread(target=cook_order).start()
        
        return kitchen_pb2.ProcessOrderResponse(
            order_id=request.order_id,
            status="COOKING",
            estimated_time=estimated_time
        )

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    kitchen_pb2_grpc.add_KitchenServiceServicer_to_server(KitchenService(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    logger.info("Kitchen Service is running on port 50052")
    server.wait_for_termination()

if __name__ == '__main__':
    serve() 