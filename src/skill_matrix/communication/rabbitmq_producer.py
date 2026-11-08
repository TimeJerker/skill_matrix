import json
import aio_pika

RABBITMQ_URL = "amqp://guest:guest@localhost:5672/"
QUEUE_NAME = "task_notifications"

async def publish_assignment_event(user_id: int, project_id: int, task_name: str):
    """
    Публикует событие о добавлении сотрудника в проект/задачу.
    """
    # 1. Подключаемся к RabbitMQ
    connection = await aio_pika.connect_robust(RABBITMQ_URL)
    async with connection:
        # 2. Создаем канал
        channel = await connection.channel()
        
        # 3. Объявляем очередь (на случай, если ее еще нет)
        queue = await channel.declare_queue(QUEUE_NAME, durable=True)
        
        # 4. Формируем тело сообщения
        payload = {
            "user_id": user_id,
            "project_id": project_id,
            "message": f"You have been added to the project: '{project_id}'!"
        }
        
        # 5. Публикуем сообщение в очередь
        await channel.default_exchange.publish(
            aio_pika.Message(
                body=json.dumps(payload).encode(),
                delivery_mode=aio_pika.DeliveryMode.PERSISTENT
            ),
            routing_key=QUEUE_NAME
        )
        print(f"[API Service] An event has been published for the user {user_id}: {payload['message']}")