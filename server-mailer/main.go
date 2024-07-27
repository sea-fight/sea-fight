package main

import (
	"crypto/tls"
	"encoding/json"
	"fmt"
	"strconv"
	"strings"

	"github.com/rabbitmq/amqp091-go"
	"github.com/sea-fight/sea-fight/server-mailer/config"
	"github.com/sea-fight/sea-fight/server-mailer/templates"
	"go.uber.org/zap"
	gomail "gopkg.in/mail.v2"
)

type Message struct {
	Receiver string            `json:"receiver"`
	Template string            `json:"template"`
	Args     map[string]string `json:"args"`
}

func main() {
	log, _ := zap.NewDevelopment()
	log.Info("Parsing templates...")
	templates := templates.New(log)
	log.Info(fmt.Sprint(len(templates), " templates successfully parsed"))
	log.Info("Connecting to SMTP...")
	smtp := newDialer()
	sender, err := smtp.Dial()
	if err != nil {
		panic(fmt.Sprint("Cannot connect to SMTP: ", err))
	}
	log.Info("SMTP connected")
	log.Info("Connecting to AMQP...")
	deliveries := listenForEvents()
	log.Info("AMQP connected, listening for events")
	for delivery := range deliveries {
		log.Info("Received message")
		msg := new(Message)
		if json.Unmarshal(delivery.Body, msg) != nil {
			log.Warn("Invalid message: " + string(delivery.Body))
			continue
		}
		template, ok := templates[msg.Template]
		if !ok {
			log.Warn("Requested invalid template: " + msg.Template)
			continue
		}
		subject, text, ok := template.Format(msg.Args)
		if !ok {
			keys := make([]string, len(msg.Args))
			for k := range msg.Args {
				keys = append(keys, k)
			}
			log.Warn(fmt.Sprint(
				"Requested template ",
				msg.Template,
				" with invalid args: ",
				strings.Join(keys, ","),
				" expected ",
				strings.Join(template.Args(), ","),
			))
			continue
		}
		mail := gomail.NewMessage()
		mail.SetHeader("From", config.EmailSender)
		mail.SetHeader("To", msg.Receiver)
		mail.SetHeader("Subject", subject)
		mail.SetBody("text/plain", text)
		err := gomail.Send(sender, mail)
		if err != nil {
			log.Error("Cannot send mail", zap.Error(err))
		}
	}
}

func listenForEvents() <-chan amqp091.Delivery {
	conn, err := amqp091.Dial(config.RabbitmqUrl)
	if err != nil {
		panic(fmt.Sprint("Cannot create connection with RabbitMQ: ", err))
	}
	channel, err := conn.Channel()
	if err != nil {
		panic(fmt.Sprint("Cannot create AMQP channel: ", err))
	}
	queue, err := channel.QueueDeclare(config.RabbitmqQueue, false, false, false, false, nil)
	if err != nil {
		panic(fmt.Sprint("Cannot declare queue: ", err))
	}
	deliveries, err := channel.Consume(queue.Name, "", true, false, false, false, nil)
	if err != nil {
		panic(fmt.Sprint("Cannot register consumer: ", err))
	}
	return deliveries
}

func newDialer() *gomail.Dialer {
	port, _ := strconv.Atoi(config.SmtpPort)
	dialer := gomail.NewDialer(config.SmtpServer, port, config.EmailSender, config.EmailSenderPassword)
	dialer.TLSConfig = &tls.Config{ServerName: config.SmtpServer}
	return dialer
}
