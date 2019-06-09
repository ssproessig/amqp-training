package main

import (
	"github.com/streadway/amqp"
	"log"
	"os"
)


const AmqpUri = "amqp://guest:guest@localhost:5672/"
const ExchangeName = "amqp-training"


func argAtIndexOrDefault(index int, defaultValue string) string {
	result := defaultValue

	if len(os.Args) > index + 1 {
		result = os.Args[index]
	}

	return result
}


func main() {
	RoutingKey := argAtIndexOrDefault(1, "#")
	QueueName := argAtIndexOrDefault(2, "go-consumer")

	connection, err := amqp.Dial(AmqpUri)
	if err != nil {
		log.Fatalf("Failed to connect to %s: %s", AmqpUri, err)
	}
	defer connection.Close()
	log.Printf("Connected to AMQP: %s", AmqpUri)


	channel, err := connection.Channel()
	if err != nil {
		log.Fatalf("Failed to acquire channel: %s", err)
	}
	defer channel.Close()


	err = channel.ExchangeDeclare(ExchangeName,"topic",false,false,false,false,nil,)
	if err != nil {
		log.Fatalf("Failed to declare exchange '%s': %s", ExchangeName, err)
	}

	_, err = channel.QueueDeclare(QueueName, false, true, false, false, nil, )
	if err != nil {
		log.Fatalf("Failed to declare queue '%s': %s", QueueName, err)
	}
	log.Printf("Using queue: %s", QueueName)


	err = channel.QueueBind(QueueName, RoutingKey, ExchangeName, false, nil)
	if err != nil {
		log.Fatalf("Failed to bind queue '%s' to exchange '%s' with '%s': %s", QueueName, ExchangeName, RoutingKey, err)
	}
	log.Printf("Bound queue '%s' to exchange '%s' with '%s'", QueueName, ExchangeName, RoutingKey)


	messages, err := channel.Consume(QueueName, "",true, false, false, false, nil)

	if err != nil {
		log.Printf("Failed to register a consumer: %s", err)
	}


	go func() {
		for d := range messages {
			log.Printf(" [x] %24s:  %s", d.RoutingKey, d.Body)
		}
	}()

	log.Printf(" [*] Waiting for messages. To exit press CTRL+C")

	forever := make(chan bool)
	<-forever
}
