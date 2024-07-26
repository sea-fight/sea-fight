package amqp

import (
	"fmt"

	rabbit "github.com/rabbitmq/amqp091-go"
)

func ListenForEvents(connectionString, queueName string) <-chan rabbit.Delivery {
	conn, err := rabbit.Dial(connectionString)
	if err != nil {
		panic(fmt.Sprint("Cannot create connection with RabbitMQ:", err))
	}
	channel, err := conn.Channel()
	if err != nil {
		panic(fmt.Sprint("Cannot create AMQP channel:", err))
	}
	queue, err := channel.QueueDeclare(queueName, false, false, false, false, nil)
	if err != nil {
		panic(fmt.Sprint("Cannot declare queue:", err))
	}
	deliveries, err := channel.Consume(queue.Name, "", true, false, false, false, nil)
	if err != nil {
		panic(fmt.Sprint("Cannot register consumer:", err))
	}
	return deliveries
}
