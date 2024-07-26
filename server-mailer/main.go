package main

import (
	"encoding/json"
	"fmt"

	"github.com/sea-fight/sea-fight/server-mailer/amqp"
)

type Message struct {
	Lang     string   `json:"lang"`
	Template string   `json:"template"`
	Payload  []string `json:"payload"`
	Receiver string   `json:"receiver"`
	Date     int64    `json:"date"`
}

func main() {
	for delivery := range amqp.ListenForEvents() {
		msg := new(Message)
		if err := json.Unmarshal(delivery.Body, msg); err != nil {
			fmt.Println("Invalid message:", string(delivery.Body))
			continue
		}
		// TODO
	}
}
