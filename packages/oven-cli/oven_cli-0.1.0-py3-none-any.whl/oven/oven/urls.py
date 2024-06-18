import logging

from oven.config import Config


class URLArchive:
    _instance = None

    def __new__(cls, config: Config = None):
        if cls._instance is None:
            cls._instance = super(URLArchive, cls).__new__(cls)
            cls._instance.__initialize(config)
        return cls._instance

    def __initialize(self, config: Config) -> None:
        self.config = config
        self.urls = {}

        for lang in self.config.locales_langs:
            self.urls[lang] = {}

    def add_url(self, node) -> None:
        for lang in self.config.locales_langs:
            if lang == self.config.locales_main:
                self.urls[lang][node.get_name()] = f'{self.config.site_root}/{node.get_output_name()}'
            else:
                self.urls[lang][node.get_name()] = f'{self.config.site_root}/_{lang}/{node.get_output_name()}'

    def get_url(self, name: str, lang: str) -> str:
        if self.urls[lang].get(name, None):
            return self.urls[lang][name]
        else:
            logging.error(f'[URLArchiver] could not find url for {name} for lang {lang}')
            return self.config.site_url + '/' + '404.html'
