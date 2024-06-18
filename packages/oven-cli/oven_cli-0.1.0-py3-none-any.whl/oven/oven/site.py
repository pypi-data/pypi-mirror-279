import json
import logging
import os

from pathlib import Path
from typing import List, Dict

from .config import Config
from .trans import Translator
from .theme import Theme
from .urls import URLArchive
from .errors import ErrorHolder


class Content:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.name = path.stem
        self.msg_id = path.parent.stem + '-' + self.name

        logging.info(f'[Content][{self.name}] loading default data')

        with open(self.path, 'r') as f:
            self.default_data = f.read()
        self.trans = {}

    def get_lang(self, lang: str) -> str:
        return self.trans.get(lang, self.default_data)

    def add_lang(self, lang: str, data: str) -> None:
        logging.info(f'[Content][{self.name}] adding {lang} lang')
        self.trans[lang] = data

    def __str__(self) -> str:
        return f'[Content][{self.name}][{self.msg_id}] = {self.default_data}'


class Node:
    CONFIG_FILE = "config.json"
    CONTEXT_FILE = "context.json"

    def __init__(self, path: Path, config: Config) -> None:
        self.config = config
        self.path = path
        self.name = self.path.stem
        self.output_name = self.name

        self.contents = []
        self.context = {}
        self._raw_config = {}

        logging.info(f'[Node][{self.name}] detected at {self.path}')
        self.__load_content()
        self.__load_context()
        if self.config.is_build_config():
            self.__load_config()

    def __load_context(self):
        logging.info(f'[Node][{self.name}] loading context')

        try:
            with open(self.path / Node.CONTEXT_FILE, encoding='utf-8', mode='r') as f:
                self.context = json.load(f)
        except FileNotFoundError:
            pass
        except Exception as e:
            ErrorHolder().add_error(e)

        self.context['this'] = self.name

    def __load_content(self) -> None:
        logging.info(f'[Node][{self.name}] loading content')

        for file in self.path.iterdir():
            if file.is_file() and file.suffix == '.md':
                self.contents.append(Content(file))

    def __load_config(self) -> None:
        logging.info(f'[Node][{self.name}] loading config')

        try:
            with open(self.path / self.CONFIG_FILE, encoding='utf-8', mode='r') as f:
                self._raw_config = json.load(f)
        except FileNotFoundError:
            pass
        except Exception as e:
            ErrorHolder().add_error(e)

        self.output_name = self._raw_config.get('output_name', self.path.stem)
        self.template_name = self._raw_config.get('template_name', self.config.default_template_name)
        self.exclude_pre_render = self._raw_config.get('exclude_pre_render', [])

    def __get_build_path(self, lang: str) -> Path:
        if lang == self.config.locales_main:
            return self.config.build_path / self.output_name
        return self.config.build_path / f'_{lang}' / self.output_name

    def __get_contents(self, lang: str) -> Dict:
        contents = {}
        for content in self.contents:
            contents[content.name] = content.get_lang(lang)
        return contents

    def __get_context(self, lang: str) -> Dict:
        context = self.context
        context['lang'] = lang
        return context

    def load_translations(self, trans: Translator) -> None:
        logging.info(f'[Node][{self.name}] loading translations')

        for lang in self.config.locales_langs:
            for content in self.contents:
                content.add_lang(lang, trans.get_text(content.msg_id, lang))
            for context_key, context_item in self.context.items():
                self.context[context_key] = trans.get_text(f'{self.name}-{context_key}', lang)

    def get_contents(self) -> List[Content]:
        return self.contents

    def output_content(self) -> None:
        logging.info(f'[Node][{self.name}] outputting content')

        theme = Theme()
        for lang in self.config.locales_langs:
            lang_build_path = self.__get_build_path(lang)
            logging.info(f'[Node][{self.name}] output content in {lang} to {lang_build_path}')

            os.makedirs(lang_build_path, exist_ok=True)
            with open(lang_build_path / 'index.html', encoding='utf-8', mode='w') as f:
                f.write(theme.render(self.template_name, self.__get_contents(lang), self.__get_context(lang),
                                     self.exclude_pre_render))

    def get_name(self) -> str:
        return self.name

    def get_output_name(self) -> str:
        return self.output_name


class Site:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.nodes = []

        self.__gather_nodes()
        logging.info(f'[Site] gathered {len(self.nodes)} nodes')

        if self.config.is_build_config():
            self.__load_translations()
        elif self.config.is_gather_config():
            self.__gather_translations()

    def __gather_nodes(self) -> None:
        logging.info(f'[Site] Gathering nodes')

        urls = URLArchive()
        for file in self.config.source_path.iterdir():
            if file.is_dir():
                node = Node(file, self.config)
                urls.add_url(node)
                self.nodes.append(node)

    def __load_translations(self) -> None:
        for node in self.nodes:
            node.load_translations(Translator())

    def __gather_translations(self) -> None:
        for node in self.nodes:
            for content in node.get_contents():
                Translator().add_text(content.msg_id, content.default_data)
            for context_key, context_item in node.context.items():
                Translator().add_text(f'{node.name}-{context_key}', context_item)
        for context_key, context_item in self.config.site_context.items():
            Translator().add_text(context_key, context_item)

    def output_content(self) -> None:
        logging.info(f'[Site] outputting {len(self.nodes)} nodes')

        for node in self.nodes:
            node.output_content()
