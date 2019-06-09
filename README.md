# Example Source Code: AMQP Training
We will have a Python __producer__ that

- publishes one sample __message__ a second with random __routing keys__ to the `amqp-training` __exchange__
- the __exchange__ itself is a __non-durable__ `topic` exchange

We then have __consumers__ in several languages that

- create __non-durable queues__ with configurable _queue names_  and
- use a configurable __routing key__ to connect this __queue__ to the `amqp-training` __exchange__

Configurable command-line interface parameters for all consumers

1. used _routing key_, defaults to `*.info`
1. used _queue name_, defaults to `<lang>-consumer`

## Preparation
Start a RabbitMQ 3 Docker container with the embedded management interface

```
> docker run --name rmq -p15672:15672 –p5672:5672 rabbitmq:3-management 
```

This gives us the default connection URI
```
amqp://guest:guest@localhost:5672/
```

Open [http://localhost:15672](http://localhost:15672) and login with `guest`/`guest` to watch the exchange and queues.


