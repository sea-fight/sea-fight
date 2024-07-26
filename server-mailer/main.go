package main

import (
	"encoding/json"
	"fmt"
	"strings"

	"github.com/emersion/go-sasl"
	"github.com/emersion/go-smtp"
	"github.com/rabbitmq/amqp091-go"
	"github.com/sea-fight/sea-fight/server-mailer/config"
	"github.com/sea-fight/sea-fight/server-mailer/localization"
)

type Message struct {
	Receiver string `json:"receiver"`
	Lang     string `json:"lang"`
	Template string `json:"template"`
	Args     []int  `json:"args"`
}

func main() {
	smtp := connectToSMTP()
	loc := localization.New()
	for delivery := range listenForEvents() {
		msg := new(Message)
		if json.Unmarshal(delivery.Body, msg) != nil {
			fmt.Println("Invalid message:", string(delivery.Body))
			continue
		}
		text, err := loc.Translate(msg.Lang, msg.Template, msg.Args)
		if err != nil {
			fmt.Println("Locale", msg.Lang, "not found")
			continue
		}
		smtp.SendMail(config.EmailSender, []string{msg.Receiver}, strings.NewReader(text))
	}
}

func listenForEvents() <-chan amqp091.Delivery {
	conn, err := amqp091.Dial(config.RabbitmqUrl)
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

func connectToSMTP() *smtp.Client {
	client, err := smtp.DialStartTLS(fmt.Sprintf("%s:%s", config.SmtpServer, config.SmtpPort), nil)
	if err != nil {
		panic(fmt.Sprint("Cannot connect to smtp:", err))
	}
	loginClient := sasl.NewLoginClient(config.EmailSender, config.EmailSenderPassword)
	if err = client.Auth(loginClient); err != nil {
		panic(fmt.Sprint("Cannot authorize client:", err))
	}
	return client
}
