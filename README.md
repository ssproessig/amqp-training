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


## Python
### Information
- tested with Python 3.6
- requires the following modules (use `pip install -r requirements.txt`)
  - `pika` `>=1.0.1`

### Source Code
- [python/producer.py](python/producer.py)
- [python/consumer.py](python/consumer.py)
- [python/amqp/__init__.py](python/amqp/__init__.py) 


## Golang
### Information
- tested with Go 1.12.5
- requires the following module (get it with `go get <dep>`)
  - `github.com/streadway/amqp`

## Source Code
- [go/consumer.go](go/consumer.go)


## Qt 5 / C++14
### Information
- tested on Windows 10 x64, WSL, macOS 10.14.5
- compiled with
  - Microsoft Visual Studio 2017 Win64, Windows 10 Enterprise N 2016 LTSB (OS Build 1493.2999)
  - gcc 6.3.0-18 and clang 8.0.0 on WSL (Debian GNU/Linux 9.9)
  - gcc on macOS

- requires the following dependencies
  - CMake >= 3.11
  - Qt 5  >= 5.7.1

- uses the very nice AMQP 0.9.1 implementation from [https://github.com/mbroadst/qamqp](https://github.com/mbroadst/qamqp)
  - uses revision [b5c660a](https://github.com/mbroadst/qamqp/commit/b5c660a1ac10ac5bbb8f770318d0eb69b484de93)
  - wrapped in CMake
  - patched `QString QAmqpClient::gitVersion()` in `qamqpclient.cpp` to always return `b5c660a`

### Source Code
- [qt/CMakeLists.txt](qt/CMakeLists.txt)
- [qt/src/consumer.cpp](qt/src/consumer.cpp)
- [qt/lib/CMakeLists.txt](qt/lib/CMakeLists.txt)
- [qt/lib/qamqp](qt/lib/qamqp)


