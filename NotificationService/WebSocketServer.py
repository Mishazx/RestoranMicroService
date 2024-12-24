from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import Dict, List, Any
import logging
import json

from database import Notification, SessionLocal

logger = logging.getLogger('WebSocketServer')

class NotificationManager:
    def __init__(self):
        self.order_connections: Dict[str, List[Dict[str, Any]]] = {}
        self.active_connections: set = set()

    async def connect(self, websocket: WebSocket, order_id: str = None):
        await websocket.accept()
        self.active_connections.add(websocket)
        
        if order_id:
            if order_id not in self.order_connections:
                self.order_connections[order_id] = []
            
            connection_info = {
                "websocket": websocket,
                "status": None
            }
            self.order_connections[order_id].append(connection_info)
            
            logger.info(f"Client connected to order {order_id}. Total connections: {len(self.active_connections)}")

            last_notification = await self.get_last_notification(order_id)
            if last_notification:
                await websocket.send_json(last_notification)

    async def disconnect(self, websocket: WebSocket, order_id: str = None):
        self.active_connections.discard(websocket)
        
        if order_id and order_id in self.order_connections:
            # Удаляем конкретное подключение для order_id
            self.order_connections[order_id] = [
                conn for conn in self.order_connections[order_id] 
                if conn['websocket'] != websocket
            ]
            
            # Удаляем ключ order_id, если больше нет подключений
            if not self.order_connections[order_id]:
                del self.order_connections[order_id]
        
        logger.info(f"Client disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        disconnected = set()
        is_picked_up = message.get('status') == 'PICKED_UP'
        
        for connection in list(self.active_connections):
            try:
                await connection.send_json(message)
                
                if is_picked_up:
                    await connection.close()
                    disconnected.add(connection)
            
            except Exception:
                disconnected.add(connection)
        
        for connection in disconnected:
            self.active_connections.discard(connection)
            
            for order_id, connections in list(self.order_connections.items()):
                self.order_connections[order_id] = [
                    conn for conn in connections 
                    if conn['websocket'] != connection
                ]
                
                if not self.order_connections[order_id]:
                    del self.order_connections[order_id]

    async def get_last_notification(self, order_id: str) -> dict:
        """ Получение последнего уведомления из базы данных для order_id. """
        db = SessionLocal()
        last_notification = (
            db.query(Notification)
            .filter(Notification.order_id == order_id)
            .order_by(Notification.created_at.desc())
            .first()
        )
        db.close()
        if last_notification:
            return {
                "order_id": last_notification.order_id,
                "table_number": last_notification.table_number,
                "status": last_notification.status,
                "message": last_notification.message,
                "timestamp": last_notification.created_at.isoformat()
            }
        return None

app = FastAPI()

notification_manager = NotificationManager()

@app.websocket("/ws/orders/{order_id}")
async def websocket_endpoint(websocket: WebSocket, order_id: str):
    await notification_manager.connect(websocket, order_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await notification_manager.disconnect(websocket, order_id)

@app.websocket("/ws/orders")
async def websocket_all_orders(websocket: WebSocket):
    await notification_manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await notification_manager.disconnect(websocket) 