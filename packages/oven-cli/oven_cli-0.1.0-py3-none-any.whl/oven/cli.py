import time
import logging
import argparse

import http.server
import socketserver

from oven.config import Config, EConfigType
from oven.trans import Translator
from oven.theme import Theme
from oven.site import Site
from oven.urls import URLArchive
from oven.scripts import ScriptsManager, EOvenScriptExecTime
from oven.errors import ErrorHolder


def build_site(args):
    logging.info("[Oven Site Build Started]")
    config = Config(args, EConfigType.BUILD)
    run(config)


def gather_trans(args):
    logging.info("[Oven Site Trans Gather Started]")
    config = Config(args, EConfigType.GATHER)
    run(config)


def serve_site(args):
    config = Config(args, EConfigType.SERVE)

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=config.build_path, **kwargs)

    with socketserver.TCPServer(("", 80), Handler) as httpd:
        logging.info("[Oven Site Server] serving at http://localhost:80")
        try:
            httpd.allow_reuse_port = True
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        httpd.server_close()


def run(config: Config) -> None:
    _start_time = time.time()

    # initialize singletons with config
    _ = URLArchive(config)
    _ = Translator(config)
    _ = Theme(config)
    _ = ErrorHolder()

    # initialize other classes
    scripts = ScriptsManager(config)

    scripts.execute(EOvenScriptExecTime.START_BUILD if config.is_build_config() else EOvenScriptExecTime.START_GATHER)
    site = Site(config)
    if config.is_build_config():
        site.output_content()
    scripts.execute(EOvenScriptExecTime.FINISH_BUILD if config.is_build_config() else EOvenScriptExecTime.FINISH_GATHER)

    logging.info(f'[Oven Site Finished] {time.time() - _start_time:.3f}s')
    errors = ErrorHolder().get_errors()
    logging.info(f'[Oven Site Finished] encountered {len(errors)} errors')
    for error in errors:
        logging.error(error)


def main():
    logging.basicConfig(level=logging.INFO, format='%(message)s')

    parser = argparse.ArgumentParser(description='oven - yet another static site generator with markdown support')
    parser.add_argument('--enable-scripts', help='Comma-separated list of scripts to enable')
    parser.add_argument('--disable-scripts', help='Comma-separated list of scripts to be')
    parser.add_argument('--force-scripts', help='Comma-separated list of scripts to override config')

    subparsers = parser.add_subparsers(help='commands')

    # Build
    build_parser = subparsers.add_parser('build', help='Build static site')
    build_parser.set_defaults(func=build_site)

    # Gather
    gather_parser = subparsers.add_parser('gather', help='`Gather translations')
    gather_parser.set_defaults(func=gather_trans)

    # Server
    server_parser = subparsers.add_parser('serve', help='Serve static site locally')
    server_parser.set_defaults(func=serve_site)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()
