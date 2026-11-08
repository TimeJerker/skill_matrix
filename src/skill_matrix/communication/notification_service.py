import asyncio
import json
from typing import Dict, List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import aio_pika
import uvicorn
from contextlib import asynccontextmanager

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
QUEUE_NAME = "task_notifications"

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[WebSocket]] = {}
        self.offline_messages: Dict[int, List[str]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        print(f"[WS] User {user_id} connected.")

        if user_id in self.offline_messages and self.offline_messages[user_id]:
            print(f"[Notification Service] Sending accumulated messages for User {user_id}...")
            for msg in self.offline_messages[user_id]:
                await websocket.send_text(msg)
            self.offline_messages[user_id].clear()

    def disconnect(self, user_id: int, websocket: WebSocket):
        if user_id in self.active_connections:
            self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        print(f"[WS] User {user_id} disconnected.")

    async def send_personal_message(self, user_id: int, message: str):
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                await connection.send_text(message)
            print(f"[Notification Service] Notification delivered to the user {user_id}")
        else:
            print(f"[Notification Service] User {user_id} currently offline. Save to the buffer.")
            if user_id not in self.offline_messages:
                self.offline_messages[user_id] = []
            self.offline_messages[user_id].append(message)
manager = ConnectionManager()

async def consume_rabbitmq_messages():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    print("[Notification Service] Successfully connected to RabbitMQ. Waiting for messages...")

    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                payload = json.loads(message.body.decode())
                user_id = payload.get("user_id")
                notification_text = payload.get("message")
                
                print(f"[Notification Service] Retrieved from RabbitMQ for User {user_id}: {notification_text}")
                
                await manager.send_personal_message(
                    user_id=user_id, 
                    message=json.dumps(payload, ensure_ascii=False)
                )

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(consume_rabbitmq_messages())
    yield
    task.cancel()

app = FastAPI(title="Notification Service", lifespan=lifespan)

@app.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: int):
    await manager.connect(user_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)

if __name__ == "__main__":
    uvicorn.run("notification_service:app", host="127.0.0.1", port=8001, reload=False)