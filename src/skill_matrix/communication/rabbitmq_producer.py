import json
import aio_pika

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
QUEUE_NAME = "task_notifications"

async def publish_assignment_event(user_id: int, project_id: int, task_name: str):

    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        channel = await connection.channel()
        
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        
        payload = {
            "user_id": user_id,
            "project_id": project_id,
            "message": f"You have been added to the project: '{project_id}'!"
        }
        
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(payload).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=QUEUE_NAME
        )
        print(f"[API Service] An event has been published for the user {user_id}: {payload['message']}")