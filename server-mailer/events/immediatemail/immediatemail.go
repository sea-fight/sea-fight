package immediatemail

const Key = "immediatemail"

type Message struct {
	Receiver string            `json:"receiver"`
	Template string            `json:"template"`
	Args     map[string]string `json:"args"`
}
