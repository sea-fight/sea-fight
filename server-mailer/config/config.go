package config

import (
	"os"
)

func env(key string) string {
	val := os.Getenv(key)
	if val == "" {
		panic("Environment variable " + key + " not set")
	}
	return val
}

var EmailSender = env("EMAIL_SENDER")
var EmailSenderPassword = env("EMAIL_SENDER_PASSWORD")
var SmtpServer = env("SMTP_SERVER")
var SmtpPort = env("SMTP_PORT")
var RabbitmqUrl = env("RABBITMQ_URL")
var RabbitmqQueue = env("RABBITMQ_QUEUE")
var TemplatesDir = env("TEMPLATES_DIR")
