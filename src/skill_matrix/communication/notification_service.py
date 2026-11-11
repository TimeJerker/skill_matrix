import asyncio
import json
from typing import Dict, List
import aio_pika
import websockets

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
QUEUE_NAME = "task_notifications"
WS_HOST = "127.0.0.1"
WS_PORT = 8001

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[int, List[websockets.WebSocketServerProtocol]] = {}
        self.offline_messages: Dict[int, List[str]] = {}

    def connect(self, user_id: int, websocket):
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        self.active_connections[user_id].append(websocket)
        print(f"[WS] User {user_id} connected.")

    def disconnect(self, user_id: int, websocket):
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        print(f"[WS] User {user_id} disconnected.")

    async def send_offline_messages(self, user_id: int, websocket):
        if user_id in self.offline_messages and self.offline_messages[user_id]:
            print(f"[WS] Sending accumulated messages for User {user_id}...")
            for msg in self.offline_messages[user_id]:
                await websocket.send(msg)
            self.offline_messages[user_id].clear()

    async def send_personal_message(self, user_id: int, message: str):
        if user_id in self.active_connections and self.active_connections[user_id]:
            for connection in self.active_connections[user_id]:
                await connection.send(message)
            print(f"[Notification Service] Notification delivered to the user {user_id}")
        else:
            print(f"[Notification Service] User {user_id} currently offline. Save to the buffer.")
            if user_id not in self.offline_messages:
                self.offline_messages[user_id] = []
            self.offline_messages[user_id].append(message)

manager = ConnectionManager()

async def ws_handler(websocket):
    user_id = None
    try:
        message = await websocket.recv()
        data = json.loads(message)
        user_id = data.get("user_id")

        manager.connect(user_id, websocket)

        await manager.send_offline_messages(user_id, websocket)

        await websocket.wait_closed()
        
    except websockets.ConnectionClosed:
        pass
    finally:
        if user_id:
            manager.disconnect(user_id, websocket)


async def consume_rabbitmq_messages():
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    channel = await connection.channel()
    await channel.set_qos(prefetch_count=10)
    queue = await channel.declare_queue(QUEUE_NAME, durable=True)

    print("[Notification Service] Successfully connected to RabbitMQ. Waiting for messages...")
    async with queue.iterator() as queue_iter:
        async for message in queue_iter:
            async with message.process():
                payload = json.loads(message.body.decode("utf-8"))
                user_id = payload.get("user_id")
                await manager.send_personal_message(
                    user_id=user_id,
                    message=json.dumps(payload, ensure_ascii=False)
                )


async def main():
    print(f"[*] Starting pure WebSocket server on ws://{WS_HOST}:{WS_PORT}...")
    
    async with websockets.serve(ws_handler, WS_HOST, WS_PORT):
        print("[+] WebSocket server successfully started!")
        await consume_rabbitmq_messages()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[!] Notification Service stopped.")