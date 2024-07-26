package config

import (
	"fmt"
	"os"
)

func env(key string) string {
	val := os.Getenv(key)
	if val == "" {
		panic(fmt.Sprint("Environment variable", key, "not set"))
	}
	return val
}

var RabbitmqUrl = env("RABBITMQ_URL")
var RabbitmqQueue = env("RABBITMQ_QUEUE")
