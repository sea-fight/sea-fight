package localization

import (
	"unknwon.dev/i18n"
)

func New() *Localization {
	store := i18n.NewStore()
	return &Localization{store}
}

type Localization struct {
	inner *i18n.Store
}

func (l *Localization) Translate(lang, template string, args []int) (string, error) {
	locale, err := l.inner.Locale(lang)
	if err != nil {
		return "", err
	}
	localeArgs := make([]any, len(args))
	for idx, val := range args {
		localeArgs[idx] = val
	}
	return locale.Translate("messages::"+template, localeArgs...), nil
}
