import jinja2
import os
import shutil
from common import log, SOURCES_FOLDER, PUBLISH_FOLDER


def ensure_directory_exists(file_path):
    directory_path = os.path.dirname(file_path)
    os.makedirs(directory_path, exist_ok=True)


def compile_page(file_path):
    page_path = os.path.relpath(file_path, SOURCES_FOLDER)
    tpl_path = page_path.replace("\\", "/")

    loader = jinja2.FileSystemLoader(searchpath=SOURCES_FOLDER)
    env = jinja2.Environment(loader=loader)
    contents = env.get_template(tpl_path).render({
        'page': os.path.basename(page_path)
    })

    output_path = os.path.join(PUBLISH_FOLDER, page_path)
    ensure_directory_exists(output_path)
    with open(output_path, "w") as file:
        file.write(contents)


def publish_file(file_path):
    if file_path.endswith(".j2"):
        pass # nothing to do
    elif file_path.endswith(".html"):
        compile_page(file_path)
    else:
        dst_path = file_path.replace(SOURCES_FOLDER, PUBLISH_FOLDER)
        ensure_directory_exists(dst_path)
        shutil.copyfile(file_path, dst_path)


def build():
    log(f"Building files in {SOURCES_FOLDER}/ ...")
    shutil.rmtree(PUBLISH_FOLDER, ignore_errors=True)
    for root, dirs, files in os.walk(SOURCES_FOLDER):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            publish_file(file_path)


if __name__ == '__main__':
    build()
