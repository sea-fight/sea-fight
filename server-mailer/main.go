package main

import (
	"encoding/json"
	"fmt"
	"github.com/rabbitmq/amqp091-go"
	"github.com/sea-fight/sea-fight/server-mailer/config"
	"github.com/sea-fight/sea-fight/server-mailer/mail"
	"github.com/sea-fight/sea-fight/server-mailer/templates"
	"go.uber.org/zap"
)

type Message struct {
	Receiver string            `json:"receiver"`
	Template string            `json:"template"`
	Args     map[string]string `json:"args"`
}

func main() {
	log, _ := zap.NewDevelopment()
	log.Info("Parsing templates...")
	tmp, err := templates.Parse(log)
	if err != nil {
		log.Fatal("Cannot parse templates", zap.Error(err))
	}
	log.Info(fmt.Sprint(tmp.Count(), " templates successfully parsed"))
	log.Info("Connecting to SMTP...")
	mailer, err := mail.ConnectEnv()
	if err != nil {
		log.Fatal("Cannot connect to SMTP", zap.Error(err))
	}
	log.Info("SMTP connected")
	log.Info("Connecting to AMQP...")
	deliveries, err := listenForEvents()
	if err != nil {
		log.Fatal("Cannot connect to AMQP", zap.Error(err))
	}
	log.Info("AMQP connected, listening for events")
	for delivery := range deliveries {
		log.Info("Received message")
		msg := new(Message)
		if json.Unmarshal(delivery.Body, msg) != nil {
			log.Warn("Invalid message structure", zap.String("body", string(delivery.Body)))
			continue
		}
		templateContext, ok := tmp.BeginContext(msg.Template)
		if !ok {
			log.Warn("Requested template that does not exist", zap.String("name", msg.Template))
			continue
		}
		templateContext.With("receiver", msg.Args["receiver"])
		templateContext.WithMany(msg.Args)
		subject, text, err := templateContext.Render()
		if err != nil {
			log.Warn("Failed to format template", zap.Error(err))
			continue
		}
		err = mailer.SendMail(msg.Receiver, subject, text)
		if err != nil {
			panic(err)
		}
	}
}

func listenForEvents() (<-chan amqp091.Delivery, error) {
	conn, err := amqp091.Dial(config.RabbitmqUrl)
	if err != nil {
		return nil, fmt.Errorf("cannot create connection with RabbitMQ: %w", err)
	}
	channel, err := conn.Channel()
	if err != nil {
		return nil, fmt.Errorf("cannot create AMQP channel: %w", err)
	}
	queue, err := channel.QueueDeclare(config.RabbitmqQueue, false, false, false, false, nil)
	if err != nil {
		return nil, fmt.Errorf("cannot declare queue: %w", err)
	}
	deliveries, err := channel.Consume(queue.Name, "", true, false, false, false, nil)
	if err != nil {
		return nil, fmt.Errorf("cannot register consumer: %w", err)
	}
	return deliveries, nil
}
