import socketserver
from http.server import SimpleHTTPRequestHandler
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from generate import build
from common import log, now, SOURCES_FOLDER, PUBLISH_FOLDER


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=PUBLISH_FOLDER, **kwargs)

    def log_message(self, format, *args):
        log(format % tuple(args))


class WatchHandler(FileSystemEventHandler):
    def on_modified(self, event):
        build()
    def on_created(self, event):
        build()
    def on_deleted(self, event):
        build()


if __name__ == '__main__':
    observer = Observer()
    observer.schedule(WatchHandler(),  path=SOURCES_FOLDER,  recursive=True)
    observer.start()

    build()
    with socketserver.TCPServer(("localhost", 1989), Handler) as httpd:
        log(f"server started at http://localhost:1989 (use CTRL+C to stop)")
        httpd.serve_forever()

    observer.join()
