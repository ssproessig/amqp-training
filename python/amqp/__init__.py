import pika


EXCHANGE_NAME = "amqp-training"


def get_amqp_connection_settings():
    return pika.ConnectionParameters(
        host='localhost',
        port=5672,
        credentials=pika.credentials.PlainCredentials(username="guest", password="guest"),
        virtual_host="/"
    )


def connect_get_channel_declare_exchange_and_return_channel():
    connection = pika.BlockingConnection(get_amqp_connection_settings())

    channel = connection.channel()
    channel.exchange_declare(
        exchange=EXCHANGE_NAME,
        exchange_type='topic'
    )

    return channel
