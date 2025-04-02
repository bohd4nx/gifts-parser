import os

import yaml


class I18nManager:
    _instance = None
    _translations = {}
    _current_locale = "en"

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(I18nManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, locale="en", locales_dir=None):
        self._current_locale = locale.lower()

        if not self._translations:
            if locales_dir is None:
                locales_dir = os.path.join(os.path.dirname(__file__), "locales")

            self._load_translations(locales_dir)

    def _load_translations(self, locales_dir):
        if not os.path.exists(locales_dir):
            os.makedirs(locales_dir, exist_ok=True)

        for filename in os.listdir(locales_dir):
            if filename.endswith('.yaml') or filename.endswith('.yml'):
                locale = os.path.splitext(filename)[0].lower()
                filepath = os.path.join(locales_dir, filename)

                with open(filepath, 'r', encoding='utf-8') as f:
                    self._translations[locale] = yaml.safe_load(f)

    def set_locale(self, locale):
        if locale.lower() in self._translations:
            self._current_locale = locale.lower()

    def get_locale(self):
        return self._current_locale

    def get(self, key, **kwargs):
        locale = self._current_locale
        if locale not in self._translations:
            locale = "ru"

        value = self._translations.get(locale, {})
        for part in key.split('.'):
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                return key

        if kwargs and isinstance(value, str):
            try:
                return value.format(**kwargs)
            except KeyError:
                return value

        return value

    def __call__(self, key, **kwargs):
        return self.get(key, **kwargs)


i18n = I18nManager()


def _(key, **kwargs):
    return i18n.get(key, **kwargs)


def get_function(key):
    def func(*args, **kwargs):
        translation = i18n.get(key)
        if callable(translation):
            return translation(*args, **kwargs)
        return translation

    return func
