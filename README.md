# test-producer (Python)
- Python 3.11+
- aio_pika для работы с RabbitMQ
- Pydantic для моделей
- asyncio
- Docker
- CI/CD с Github Actions
  
test-producer отправляет 2 типа сообщений:
```
{"datetime_now": datetime}
```
где datetime - текущая дата и время (в utc)


```
{"id" : i , "value": j}
```
где i - автоинкремент (идентификатор сообщения), прибавляющий 1 к значению с каждым новым сообщением.
j – случайное целочисленное число.

### Переменные окружения:
```
# RabbitMQ
RABBITMQ_HOST=localhost
RABBITMQ_PORT=5672
RABBITMQ_USERNAME=guest
RABBITMQ_PASSWORD=guest
RABBITMQ_EXCHANGE=message-exchange
RABBITMQ_QUEUE=message-queue
RABBITMQ_ROUTING_KEY=message-routing-key

# Настройки отправителя
DATETIME_INTERVAL=10.0  # интервал в секундах для сообщений с датой
VALUE_INTERVAL=5.0      # интервал для сообщений с значением

# Логирование
LOG_LEVEL=INFO
```

### Направления дальнейшего развития/улучшения:
- Написание интеграционных тестов (для RabbitMQ)
- Механизм доставки сообщений и повторная отправка неудавшихся
- Добавление новых сообщений для отправки, реализация для них сервисов отправки
- Брать данные откуда то, а не генерировать (например с бд/чата и т.д)

![изображение](https://github.com/user-attachments/assets/7009630e-9f5c-417d-a74e-2bfe9f4dca19)
