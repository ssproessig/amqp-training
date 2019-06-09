#!/usr/bin/env python
import time
from random import choice
from string import ascii_lowercase

from amqp import connect_get_channel_declare_exchange_and_return_channel, EXCHANGE_NAME

APPS = ["foo", "bar", "infrastructure"]
LEVELS = ["debug", "info", "warn", "error"]


def publish_cyclically():
    channel = connect_get_channel_declare_exchange_and_return_channel()

    for counter in range(1, 1000):
        routing_key = "%s.%s" % (choice(APPS), choice(LEVELS))
        body = "%03d  Some random text: %s " % (
            counter,
            ''.join(choice(ascii_lowercase) for _ in range(16))
        )

        channel.basic_publish(
            exchange=EXCHANGE_NAME,
            routing_key=routing_key,
            body=body
        )
        print("Published '%s' to '%s' with routing-key '%s'." % (body, EXCHANGE_NAME, routing_key))

        time.sleep(1)


if __name__ == "__main__":
    try:
        publish_cyclically()

    except KeyboardInterrupt:
        pass
