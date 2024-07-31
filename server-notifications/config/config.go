package config

import (
	"os"
	"strconv"
)

func env(key string) string {
	val := os.Getenv(key)
	if val == "" {
		panic("Environment variable " + key + " not set")
	}
	return val
}

func envInt(key string) int {
	v := env(key)
	i, err := strconv.Atoi(v)
	if err != nil {
		panic(err)
	}
	return i
}

var EmailUsername = env("EMAIL_USERNAME")
var EmailPassword = env("EMAIL_PASSWORD")
var EmailAddress = env("EMAIL_ADDRESS")
var SmtpServer = env("SMTP_SERVER")
var SmtpPort = envInt("SMTP_PORT")

var RabbitmqUrl = env("RABBITMQ_URL")
var RabbitmqQueue = env("RABBITMQ_QUEUE")
var TemplatesDir = env("TEMPLATES_DIR")
