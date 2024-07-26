package amqp

import (
	"fmt"

	rabbit "github.com/rabbitmq/amqp091-go"
	"github.com/sea-fight/sea-fight/server-mailer/config"
)

func ListenForEvents() <-chan rabbit.Delivery {
	conn, err := rabbit.Dial(config.RabbitmqUrl)
	if err != nil {
		panic(fmt.Sprint("Cannot create connection with RabbitMQ:", err))
	}
	channel, err := conn.Channel()
	if err != nil {
		panic(fmt.Sprint("Cannot create AMQP channel:", err))
	}
	queue, err := channel.QueueDeclare(config.RabbitmqQueue, false, false, false, false, nil)
	if err != nil {
		panic(fmt.Sprint("Cannot declare queue:", err))
	}
	deliveries, err := channel.Consume(queue.Name, "", true, false, false, false, nil)
	if err != nil {
		panic(fmt.Sprint("Cannot register consumer:", err))
	}
	return deliveries
}
