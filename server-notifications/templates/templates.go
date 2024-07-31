package templates

import (
	"errors"
	"fmt"
	"maps"
	"os"
	"path"
	"regexp"
	"strings"

	"github.com/sea-fight/sea-fight/server-notifications/config"
	"go.uber.org/zap"
)

type Template struct {
	args []string
	text string
}

type missingArgsError struct {
	Args []string
}

func (e *missingArgsError) Error() string {
	return fmt.Sprint("missing args: ", strings.Join(e.Args, ", "))
}

var ErrTemplateMalformed = errors.New("template malformed after processing")

func (t *Template) fmt(other map[string]string) (subject string, body string, err error) {
	missingArgs := make([]string, 0)
	for _, val := range t.args {
		_, ok := other[val]
		if !ok {
			missingArgs = append(missingArgs, val)
		}
	}
	if len(missingArgs) > 0 {
		return "", "", &missingArgsError{missingArgs}
	}
	text := t.text
	for _, val := range t.args {
		text = strings.ReplaceAll(text, "{"+val+"}", other[val])
	}
	subject, body, ok := strings.Cut(text, "\n\n")
	if !ok {
		return "", "", ErrTemplateMalformed
	}
	return subject, body, nil
}

var re = regexp.MustCompile(`\{([a-z]+)}`)

func Parse(log *zap.Logger) (*Templates, error) {
	result := make(map[string]*Template)
	entries, err := os.ReadDir(config.TemplatesDir)
	if err != nil {
		return nil, fmt.Errorf("cannot read templates directory: %w", err)
	}
	for _, entry := range entries {
		templateName := entry.Name()[:strings.IndexByte(entry.Name(), '.')]
		fullPath := path.Join(config.TemplatesDir, entry.Name())
		bytes, err := os.ReadFile(fullPath)
		if err != nil {
			return nil, fmt.Errorf("cannot read file: %w", err)
		}
		argsDef, text, _ := strings.Cut(string(bytes), "\n\n")
		argsDefMap := make(map[string]bool)
		for _, v := range strings.Split(argsDef, ",") {
			argsDefMap[v] = true
		}
		matches := re.FindAllStringSubmatch(text, -1)
		argsMap := make(map[string]bool)
		for _, val := range matches {
			argsMap[val[1]] = true
		}
		if !maps.Equal(argsDefMap, argsMap) {
			return nil, fmt.Errorf("args in %s template definition and its content does not match", templateName)
		}
		args := make([]string, 0, len(argsMap))
		for k := range argsMap {
			args = append(args, k)
		}
		log.Info("Registered template " + templateName)
		result[templateName] = &Template{
			args: args,
			text: text,
		}
	}
	return &Templates{result}, nil
}

type Templates struct {
	inner map[string]*Template
}

func (t *Templates) Count() int {
	return len(t.inner)
}

func (t *Templates) CreateContext(templateName string) (*TemplateContext, bool) {
	tmp, ok := t.inner[templateName]
	if !ok {
		return nil, false
	}
	return &TemplateContext{tmp, make(map[string]string)}, true
}

type TemplateContext struct {
	tmp  *Template
	args map[string]string
}

func (t *TemplateContext) With(key, value string) {
	t.args[key] = value
}

func (t *TemplateContext) WithMany(kv map[string]string) {
	maps.Copy(t.args, kv)
}

func (t *TemplateContext) Render() (string, string, error) {
	return t.tmp.fmt(t.args)
}
