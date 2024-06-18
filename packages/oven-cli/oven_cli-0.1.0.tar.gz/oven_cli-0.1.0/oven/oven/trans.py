import os
import atexit
import logging

import polib

from .config import Config


class Translator:
    _instance = None

    def __new__(cls, config: Config = None):
        if cls._instance is None:
            cls._instance = super(Translator, cls).__new__(cls)
            cls._instance.__initialize(config)
            atexit.register(cls._instance.__del__)  # force destructor with singleton pattern
        return cls._instance

    def __initialize(self, config: Config):
        self._gathered_texts = 0

        self.config = config
        self.po_files = {}
        self.__load_po_files()

    def __del__(self):
        if self.config.is_gather_config():
            self.__save_po_files()
            logging.info(f"[Translator] Gathered {self._gathered_texts} translations.")

    def __load_po_files(self):
        logging.info(f'[Translator] loading .po files for {self.config.locales_langs}')
        os.makedirs(self.config.locales_path, exist_ok=True)

        for lang in self.config.locales_langs:
            po_file_path = self.config.locales_path / f'{lang}.po'
            if po_file_path.exists():
                self.po_files[lang] = polib.pofile(str(po_file_path))
            else:
                self.po_files[lang] = polib.POFile()

    def __save_po_files(self):
        logging.info(f'[Translator] saving .po files for {self.config.locales_langs}')
        for lang in self.config.locales_langs:
            po_file_path = self.config.locales_path / f'{lang}.po'
            self.po_files[lang].save(str(po_file_path))

    def add_text(self, msgid: str, msgstr: str):
        self._gathered_texts += 1
        default_entry = self.po_files[self.config.locales_main].find(msgid) or polib.POEntry(msgid=msgid, msgstr='')
        for lang in self.config.locales_langs:
            entry = self.po_files[lang].find(msgid)
            if not entry:
                entry = polib.POEntry(msgid=msgid, msgstr=msgstr)
                self.po_files[lang].append(entry)
            if lang == self.config.locales_main:
                entry.msgstr = msgstr
            elif entry.msgstr != default_entry.msgstr:
                entry.flags = ['fuzzy']

    def get_text(self, msgid: str, lang: str):
        entry = self.po_files[lang].find(msgid)
        if not entry or not entry.msgstr:
            return ''
        return entry.msgstr
