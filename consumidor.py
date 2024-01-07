import json
import pika

class RabbitmqConsumer:
    def __init__(self, callback) -> None:
        self.__host = "localhost"
        self.__port = "5672"
        self.__username = "guest"
        self.__password = "guest"
        self.__queue = "data_queue"
        self.__callback = callback
        self.__channel = self.__create_channel()

    def __create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username=self.__username,
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()
        channel.queue_declare(
            queue=self.__queue,
            durable=True,
            
        )
        channel.basic_consume(
            queue=self.__queue,
            auto_ack=True,
            on_message_callback=self.__callback
        )

        return channel

    def start(self):
        print(f'Listen RabbitMQ on Port 5672')
        self.__channel.start_consuming()

def minha_callback(ch, method, properties, body):
    try:
        decoded_body = body.decode("utf-8")
        parsed_data = json.loads(decoded_body)
        
        if 'mensagem' in parsed_data:
            greeting_message = parsed_data['mensagem']
            print(greeting_message)
        else:
            print("Mensagem não tem formato esperado.")

    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")

def iniciar_consumidor():
    rabbitmq_consumer = RabbitmqConsumer(minha_callback)
    rabbitmq_consumer.start()