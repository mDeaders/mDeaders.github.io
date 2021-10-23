from datetime import datetime


def now():
    return datetime.now().strftime("%H:%M:%S")


def log(message):
    print(f"{now()} - {message}", flush=True)


SOURCES_FOLDER = "sources"
PUBLISH_FOLDER = "docs"
