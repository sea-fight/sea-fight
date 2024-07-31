package mail

import (
	"github.com/sea-fight/sea-fight/server-notifications/config"
	gomail "gopkg.in/mail.v2"
)

type Config struct {
	Host        string
	Port        int
	Username    string
	Password    string
	FromAddress string
}

func Connect(c Config) (*Mailer, error) {
	d := gomail.NewDialer(c.Host, c.Port, c.Username, c.Password)
	sender, err := d.Dial()
	if err != nil {
		return nil, err
	}
	return &Mailer{sender, c.FromAddress}, nil
}

func ConnectEnv() (*Mailer, error) {
	return Connect(Config{
		Host:        config.SmtpServer,
		Port:        config.SmtpPort,
		Username:    config.EmailUsername,
		Password:    config.EmailPassword,
		FromAddress: config.EmailAddress,
	})
}

type Mailer struct {
	sc          gomail.SendCloser
	fromAddress string
}

func (m *Mailer) SendMail(to, subject, body string) error {
	msg := gomail.NewMessage()
	msg.SetHeader("From", m.fromAddress)
	msg.SetHeader("To", to)
	msg.SetHeader("Subject", subject)
	msg.SetBody("text/plain", body)
	return m.sc.Send(m.fromAddress, []string{to}, msg)
}
