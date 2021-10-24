import os
import socketserver
from http.server import SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from engine import generator
from engine.utils import debounce, log, InternalError
from engine.constants import *


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PATH_TO_PUBLISH, **kwargs)

    def log_message(self, format, *args):
        log(format % tuple(args))


class WatchHandler(FileSystemEventHandler):
    @debounce(1)
    def build(self, file_path):
        try:
            if file_path.startswith(PATH_TO_PAGES) or file_path.startswith(PATH_TO_TRANSLATIONS):
                generator.build_page(os.path.basename(file_path))
            elif file_path.startswith(PATH_TO_PARTIALS):
                generator.build_all()
            elif file_path.startswith(PATH_TO_ASSETS):
                generator.copy_static_assets()
        except InternalError as err:
            log(f"ERROR: {err}")

    def on_created(self, event):
        if os.path.isfile(event.src_path):
            self.build(event.src_path)

    def on_modified(self, event):
        if os.path.isfile(event.src_path):
            self.build(event.src_path)

    def on_deleted(self, event):
        pass


def run(port):
    observer = Observer()
    observer.schedule(WatchHandler(),  path=PATH_TO_SOURCES,  recursive=True)
    observer.start()

    generator.build_all()
    with socketserver.TCPServer(("localhost", port), Handler) as httpd:
        log(f"Server started at http://localhost:{port} (use CTRL+C to stop)")
        httpd.serve_forever()

    observer.join()
