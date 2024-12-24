import sys
from concurrent import futures
import logging
import uuid
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('OrderService')

logger.info("ORDER SERVICE IMPORTS CHECK:")
try:
    import grpc
    logger.info("✓ grpc imported successfully")
except ImportError as e:
    logger.error(f"✕ Failed to import grpc: {e}")

try:
    import pb2.order_pb2 as order_pb2
    logger.info("✓ order_pb2 imported successfully")
except ImportError as e:
    logger.error(f"✕ Failed to import order_pb2: {e}")

try:
    import pb2.order_pb2_grpc as order_pb2_grpc
    logger.info("✓ order_pb2_grpc imported successfully")
except ImportError as e:
    logger.error(f"✕ Failed to import order_pb2_grpc: {e}")

try:
    import pb2.kitchen_pb2 as kitchen_pb2
    import pb2.kitchen_pb2_grpc as kitchen_pb2_grpc
    logger.info("✓ kitchen_pb2 and kitchen_pb2_grpc imported successfully")
except ImportError as e:
    logger.error(f"✕ Failed to import kitchen proto files: {e}")

try:
    import pb2.notification_pb2 as notification_pb2
    import pb2.notification_pb2_grpc as notification_pb2_grpc
    logger.info("✓ notification_pb2 and notification_pb2_grpc imported successfully")
except ImportError as e:
    logger.error(f"✕ Failed to import notification proto files: {e}")

class OrderService(order_pb2_grpc.OrderServiceServicer):
    def __init__(self):
        self.orders = {}
        self.kitchen_channel = grpc.insecure_channel('kitchen_service:50052')
        self.kitchen_stub = kitchen_pb2_grpc.KitchenServiceStub(self.kitchen_channel)
        self.notification_channel = grpc.insecure_channel('notification_service:50053')
        self.notification_stub = notification_pb2_grpc.NotificationServiceStub(self.notification_channel)
        logger.info("Order Service initialized")

    def CreateOrder(self, request, context):
        logger.info("Received CreateOrder request")
        logger.info(f"Request table_number: {request.table_number}")
        logger.info(f"Request items: {request.items}")
        for item in request.items:
            logger.info(f"Request item - id: {item.id}, name: {item.name}, quantity: {item.quantity}")
        try:            
            order_id = str(uuid.uuid4())
            created_at = datetime.now().isoformat()
            
            # Создаем заказ
            logger.info("Creating Order object")
            order = order_pb2.Order(
                order_id=order_id,
                table_number=request.table_number,
                items=request.items,
                status=order_pb2.OrderStatus.PENDING,
                created_at=created_at
            )
            logger.info(f"Order created: {order}")
            
            # Сохраняем заказ
            self.orders[order_id] = order
            
            # Convert MenuItem from order_pb2 to kitchen_pb2
            logger.info("Converting MenuItem to kitchen_pb2 format")

            # logger.info(f"Order items: {kitchen_pb2.MenuItem.__dir__}")

            kitchen_items = [
                kitchen_pb2.MenuItem(
                    id=item.id,
                    name=item.name,
                    quantity=item.quantity
                ) for item in request.items
            ]
            logger.info(f"Converted kitchen_items: {kitchen_items}")
            
            kitchen_request = kitchen_pb2.ProcessOrderRequest(
                order_id=order_id,
                table_number=str(request.table_number),  # Convert table_number to string
                items=kitchen_items  # Use converted items
            )
            logger.info(f"Kitchen request: {kitchen_request}")
            
            # Отправляем заказ на кухню
            logger.info("Sending order to kitchen service")
            try:
                kitchen_response = self.kitchen_stub.ProcessOrder(kitchen_request)
                logger.info(f"Kitchen response: {kitchen_response}")
                
                # Обновляем статус заказа
                order.status = order_pb2.OrderStatus.COOKING
                logger.info(f"Order status updated to COOKING: {order}")
                
                # Отправляем уведомление
                notification_request = notification_pb2.OrderStatusNotification(
                    order_id=order_id,
                    table_number=str(request.table_number),
                    status=order_pb2.OrderStatus.Name(order.status),
                    message=f"Order is being cooked. Estimated time: {kitchen_response.estimated_time} minutes"
                )
                self.notification_stub.NotifyOrderStatus(notification_request)
                logger.info(f"Notification sent for order {order_id}")
                
            except grpc.RpcError as e:
                logger.error(f"Error communicating with services: {str(e)}")
                # Продолжаем выполнение, так как заказ все равно создан
            
            # Создаем ответ
            response = order_pb2.CreateOrderResponse(
                order_id=order.order_id,
                table_number=order.table_number,
                items=order.items,
                status=order.status,
                created_at=order.created_at
            )
            
            logger.info(f"Created order: {response}")
            return response
            
        except Exception as e:
            import traceback
            logger.error(f"Error creating order: {str(e)}")
            logger.error(traceback.format_exc())
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"Internal error: {str(e)}")
            return order_pb2.CreateOrderResponse()

    def GetOrder(self, request, context):
        order_id = request.order_id
        order = self.orders.get(order_id)
        
        if not order:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Order not found')
            return order_pb2.Order()
        
        return order

    def UpdateOrderStatus(self, request, context):
        order_id = request.order_id
        if order_id not in self.orders:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Order not found')
            return order_pb2.Order()

        order = self.orders[order_id]
        old_status = order.status
        order.status = request.status
        
        # Отправляе�� уведомление о смене статуса
        try:
            notification_request = notification_pb2.OrderStatusNotification(
                order_id=order_id,
                table_number=str(order.table_number),
                status=order_pb2.OrderStatus.Name(order.status),
                message=f"Order status changed from {order_pb2.OrderStatus.Name(old_status)} to {order_pb2.OrderStatus.Name(order.status)}"
            )
            self.notification_stub.NotifyOrderStatus(notification_request)
            logger.info(f"Notification sent for order {order_id} status update")
        except grpc.RpcError as e:
            logger.error(f"Failed to send notification: {str(e)}")
        
        return order
    
    def ConfirmOrderPickup(self, request, context):
        order_id = request.order_id
        if order_id not in self.orders:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details('Order not found')
            return order_pb2.Order()

        order = self.orders[order_id]
        old_status = order.status
        order.status = order_pb2.OrderStatus.PICKED_UP

        try:
            notification_request = notification_pb2.OrderStatusNotification(
                order_id=order_id,
                table_number=str(order.table_number),
                status=order_pb2.OrderStatus.Name(order.status),
                message=f"Order status changed from {order_pb2.OrderStatus.Name(old_status)} to {order_pb2.OrderStatus.Name(order.status)}"
            )
            self.notification_stub.NotifyOrderStatus(notification_request)
            logger.info(f"Notification sent for order {order_id} pickup confirmation")
        except grpc.RpcError as e:
            logger.error(f"Failed to send notification: {str(e)}")

        return order

def serve():
    logger.info("Starting Order Service...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    order_pb2_grpc.add_OrderServiceServicer_to_server(OrderService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("Order Service is running on port 50051")
    server.wait_for_termination()