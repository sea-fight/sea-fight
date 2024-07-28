package templates

import (
	"errors"
	"fmt"
	"os"
	"path"
	"strings"

	"github.com/sea-fight/sea-fight/server-mailer/config"
	"go.uber.org/zap"
)

type Template struct {
	args []string
	text string
}

var ErrInvalidArgs = errors.New("invalid arguments")
var ErrMalformedTemplate = errors.New("malformed template")

func (t *Template) Format(other map[string]string) (string, string, error) {
	if len(t.args) != len(other) {
		return "", "", ErrInvalidArgs
	}
	for _, val := range t.args {
		_, ok := other[val]
		if !ok {
			return "", "", ErrInvalidArgs
		}
	}
	text := t.text
	for _, val := range t.args {
		text = strings.ReplaceAll(text, "{"+val+"}", other[val])
	}
	subject, body, ok := strings.Cut(text, "\n\n")
	if !ok {
		return "", "", ErrMalformedTemplate
	}
	return subject, body, nil
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
		templateName := entry.Name()[:strings.IndexByte(entry.Name(), '.')]
		args, text, ok := strings.Cut(string(bytes), "\n\n")
		if !ok {
			panic("Template " + templateName + " is malformed")
		}
		log.Info("Registered template " + templateName)
		result[templateName] = &Template{
			args: strings.Split(args, ","),
			text: text,
		}
	}
	return result
}
