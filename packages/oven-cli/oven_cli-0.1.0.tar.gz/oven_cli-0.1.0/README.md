# oven
Yet another static site generator powered by markdown, because I didn't like the other stuff

It tries to follow the [K.I.S.S](https://en.wikipedia.org/wiki/KISS_principle) principle.

## Installation
For now there is no python package that can be installed. Use repository instead.

## Usage
### Config
#### Site configuration
Oven loads configuration from `oven.json` file. All the options are optional. Config is provided to every jinja2 template as `config` object.
Configured directories unless specified otherwise will be used relative to `CWD`.

##### `source_dir`
Specifies directory with site source files.
##### `build_dir`
Specifies directory of the built site output.
##### `static_dir`
Specifies subdirectory inside `build_dir` that will contain all the static assets.
##### `theme_dir`
Specifies directory with jinja2 templates.
##### `default_template_name`
Specifies default template used with pages that don't override this themselves.
##### `locales_dir`
Specifies directory with .po files containing translations.
##### `locales_main`
Specifies main (default) language for the site.
##### `locales_langs`
Specifies all languages in which the site should be translated (should include the main as well)
##### `filters_dir`
Specifies directory with custom filters (see below).
##### `enabled_filters`
Specifies enabled filters. If empty all found filters will be enabled.
##### `scripts_dir`
Specifies directory with custom scripts (see below).
##### `enabled_scripts`
Specifies enabled scripts. If empty all found scripts will be enabled.
##### `extensions_dir`
Specifies directory with custom markdown extensions (see below).
##### `enabled_extensions`
Specifies enabled extensions. If empty all found extensions will be enabled.
##### `site_url`
Specifies url for the site.
##### `site_timezone`
Specifies timezone used for the site.

#### Page configuration
Every page can be additionally configured by providing `config.json` file in its directory.
##### `template_name`
Overrides template file used for the page
##### `output_name`
Overrides output directory of the page (by default it will be the same as source).

### Gathering
```bash
python -m oven gather
```

### Building
```bash
python -m oven build
```

## Features
### Generating
Oven iterates over directories in `source_dir`. Every page should have its own, separate folder containing `.md` files and optional `context.json` and `config.json` files.

Each `.md` file will be passed to template as a context variable, named like the file.

### Translations
Oven has built-in translation features. It uses `.po` files. You can update them with `gather`, which gathers texts from .md files and all templates.

For now there is no support for localized assets.

### Filters
Custom jinja2 filters can be defined in the `filters_dir` folder. Every filter should be a separate python file
that defines the filter function named `custom_filter` and a variable containing the name of the filter named `FILTER_NAME`.

List of internally shipped filters:
* `get_text` - provides integration with oven translation both during gather and build.
* `get_url` - provides integration with resolving urls for oven pages and static files.

##### Example
This is an example custom filter from `oven/internal_scripts/curent_time.py` file.

```python
from typing import Optional

from oven.trans import Translator


FILTER_NAME = 'gettext'


def custom_filter(msgid: str, msgstr: Optional[str] = '', lang: Optional[str] = 'en') -> str:
    trans = Translator()

    if trans.config.is_gather_config():
        trans.add_text(msgid, msgstr)
        return ''
    return trans.get_text(msgid, lang)
```

### Extensions
You can define custom markdown extensions in the `extensions_dir` folder. Additional extension names, not found by the oven system, will be passed directly.

List of internally shipped extensions:
* `oven_urls` - Extension replaces non-absolute urls with jinja2 filter `get_url` that handles resolving them.

#### Example
This is an example extension in the ```oven/internal_extensions/oven_urls.py``` file that changes urls into custom resolved ones.

```python
from urllib.parse import urlparse
import xml.etree.ElementTree as etree

from markdown import Markdown, Extension
from markdown.treeprocessors import Treeprocessor


class OvenURLsProcessor(Treeprocessor):
    def run(self, root: etree):
        self.__update_links(root)

    def __update_links(self, node: etree.Element):
        if node.attrib.get('href'):
            url = urlparse(node.attrib['href'])
            if not url.netloc:
                node.attrib['href'] = '{{ ' + f'\'{node.attrib["href"]}\' | geturl(lang)' + ' }}'
        elif node.attrib.get('src'):
            url = urlparse(node.attrib['src'])
            if not url.netloc:
                node.attrib['src'] = '{{ ' + f'\'{node.attrib["src"]}__asset\' | geturl(lang)' + ' }}'
        for child in node:
            self.__update_links(child)


class OvenURLsExtension(Extension):
    def extendMarkdown(self, md: Markdown) -> None:
        md.treeprocessors.register(OvenURLsProcessor(md), EXTENSION_NAME, 1)


def makeExtension(**kwargs):
    return OvenURLsExtension(**kwargs)


EXTENSION_NAME = "oven_urls"
EXTENSION_CLASS = OvenURLsExtension
```

### Scripts
You can define scripts in the `script_dir` folder, that will be automatically detected.
For now, they are executed before/after the site is generated, but I have an idea of creating markings for different
pipeline stages that scripts could register themselves in.

In config file you can specify custom script configuration, that will be passed to `execute_script` function as `**kwargs`:
```json
{
  "scripts_config": {
    "robots.txt": {
      "output_file": "robots.txt"
    },
    "sitemap.xml": {
      "ignore_paths": [
        "_archive"
      ]
    },
    "clean": {
      "ignore_paths": [
        "_archive"
      ]
    },
    "archive": {
      "ignore_paths": [
        "_archive"
      ],
      "generate_zip": true,
      "zip_dir": "_archive",
      "generate_raw": true,
      "raw_dir": "_archive"
    },
    "assets": {
      "ignore_paths": [
        "build"
      ],
      "types": [
        ".css",
        ".js",
        ".png",
        ".otf",
        ".pdf",
        ".svg"
      ]
    }
  }
}
```

List of internally shipped extensions:
* `archive` - script that creates archives of built page, either as .zip files or as accessible in `build_dir` raw copies.
* `assets` - scripts that gathers and copies static files into the `build_dir`.
* `clean` - script that performs cleaning before building the site.
* `robots.txt` - script creates `robots.txt` file after build is complete.
* `sitemap.xml` - script creates `sitemap.xml` file after build is complete.

#### Example
This is an example script in the ```oven/internal_scripts/sitemap.py``` file. It generates `sitemap.xml` file after the
site has been generated.

```python
import logging
from typing import List
from pathlib import Path
from datetime import datetime
from xml.etree import ElementTree as ET

import pytz

from oven.utils import EOvenScriptExecTime
from oven.config import Config

SCRIPT_NAME = 'sitemap.xml'
SCRIPT_EXEC_TIME = EOvenScriptExecTime.FINISH_BUILD
SCRIPT_ORDER = 1


def parse_date(date: datetime, timezone: str) -> str:
    tz = pytz.timezone(timezone)
    return str(tz.localize(date))


def build_sitemap(path: Path, ignore_paths: List[str], url: str, timezone: str) -> ET.ElementTree:
    sitemap = ET.Element('urlset', xmlns='https://www.sitemaps.org/schemas/sitemap/0.9')

    def transform_ignore_path(ignore_path: str) -> Path:
        return path / ignore_path
    ignore_paths = list(map(transform_ignore_path, ignore_paths))

    def iter_build_sitemap(current_dir: Path):
        for entry in current_dir.iterdir():
            if entry in ignore_paths:
                continue
            elif entry.is_dir():
                iter_build_sitemap(entry)
            elif entry.is_file():
                file_url = str(entry).replace(str(path), url)

                url_element = ET.SubElement(sitemap, 'url')
                loc_element = ET.SubElement(url_element, 'loc')
                loc_element.text = file_url
                lastmod_element = ET.SubElement(url_element, 'lastmod')
                lastmod_element.text = parse_date(datetime.fromtimestamp(entry.stat().st_mtime), timezone)

    iter_build_sitemap(path)
    tree = ET.ElementTree(sitemap)
    ET.indent(tree, space='\t')
    return tree


def execute_script(config: Config, **kwargs) -> None:
    output_file = 'sitemap.xml'
    ignore_paths = kwargs.get('ignore_paths', [])

    logging.info(f'[{SCRIPT_NAME}] generating {output_file} file')
    build_sitemap(config.build_path, ignore_paths, config.site_url, config.site_timezone).write(
        config.build_path / output_file, encoding='utf-8')
```

#### Managing scripts from arguments
Some scripts should only be run from time to time, not for every build (like an archive script). We can manually override `enabled_scripts` configuration with arguments:

* `--enable-scripts` - comma seperated list of scripts names that will be appended to ones read from config
* `--disable-scripts` - comma seperated list of scripts names that will be removed from ones read from config
* `--force-scripts` - comma seperated list of scripts names that will override ones from config

## Issues
### Tests
There are no tests in place. I don't believe in unit testing...nah, I'm just a bit lazy. They'll come in time.
### Usability
Code and features flexibility is a bit iffy from UX standpoint. This should be resolved over time, as I use the system
and expand on it more.
### Performance
There are areas in code where unnecessary work is done. Some parts of it can be optimized by simply having a better architecture.

## Contributions
I'm very open to contributions for anything: features, enhancements or refactors.
If some code seems ~~stupid~~ like it use an improvement please don't hesitate to add a new issue
or pull request yourself if you will.

