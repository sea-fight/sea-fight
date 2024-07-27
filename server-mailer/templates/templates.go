package templates

import (
	"fmt"
	"os"
	"path"
	"strings"

	"github.com/sea-fight/sea-fight/server-mailer/config"
	"go.uber.org/zap"
)

type Template struct {
	args    []string
	subject string
	text    string
}

func (t *Template) Format(other map[string]string) (string, string, bool) {
	if len(t.args) != len(other) {
		return "", "", false
	}
	for _, val := range t.args {
		_, ok := other[val]
		if !ok {
			return "", "", false
		}
	}
	subject := t.subject
	for k, v := range other {
		subject = strings.ReplaceAll(subject, "{"+k+"}", v)
	}
	text := t.text
	for k, v := range other {
		text = strings.ReplaceAll(text, "{"+k+"}", v)
	}
	return subject, text, true
}

func (t *Template) Args() []string {
	r := make([]string, len(t.args))
	copy(r, t.args)
	return r
}

func New(log *zap.Logger) map[string]*Template {
	result := make(map[string]*Template)
	entries, err := os.ReadDir(config.TemplatesDir)
	if err != nil {
		panic(fmt.Sprint("Cannot read templates directory: ", err))
	}
	for _, entry := range entries {
		fullPath := path.Join(config.TemplatesDir, entry.Name())
		bytes, err := os.ReadFile(fullPath)
		if err != nil {
			panic(fmt.Sprint("Cannot read file: ", err))
		}
		parts := strings.SplitN(string(bytes), "\n\n", 3)
		templateName := entry.Name()[:strings.IndexByte(entry.Name(), '.')]
		log.Info("Registered template " + templateName)
		result[templateName] = &Template{
			args:    strings.Split(parts[0], ","),
			subject: parts[1],
			text:    parts[2],
		}
	}
	return result
}
