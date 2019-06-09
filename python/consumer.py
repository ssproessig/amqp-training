#!/usr/bin/env python
import sys

from amqp import EXCHANGE_NAME
from amqp import connect_get_channel_declare_exchange_and_return_channel


if __name__ == "__main__":
    DEBUG = False
    ROUTING_KEY = "*.info" if len(sys.argv) < 2 else sys.argv[1]
    QUEUE_NAME = "" if len(sys.argv) < 3 else sys.argv[2]

    channel = connect_get_channel_declare_exchange_and_return_channel()

    queue = channel.queue_declare(
        queue=QUEUE_NAME,
        auto_delete=True,
    )
    QUEUE_NAME = queue.method.queue

    channel.queue_bind(
        queue=QUEUE_NAME,
        exchange=EXCHANGE_NAME,
        routing_key=ROUTING_KEY
    )

    print("Waiting for messages routed to '%s' with binding-key '%s' from '%s'. "
          "To exit press CTRL+C" % (QUEUE_NAME, ROUTING_KEY, EXCHANGE_NAME))


    def callback(ch, method, properties, body):
        print("-" * 80)
        if DEBUG:
            print("     Channel: %s" % ch)
            print("     Method: %s" % method)
            print("     Properties: %s" % properties)
            print("")
        print("     Routing-Key: '%s'" % method.routing_key)
        print("     Body %r" % body)


    channel.basic_consume(
        queue=QUEUE_NAME,
        auto_ack=True,
        on_message_callback=callback
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        pass
