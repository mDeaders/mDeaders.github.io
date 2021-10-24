import jinja2
import os
import shutil

from engine.constants import *
from engine.i18n import I18n
from engine.utils import log


def ensure_directory_exists(file_path):
    directory_path = os.path.dirname(file_path)
    os.makedirs(directory_path, exist_ok=True)


def compile_template(file_name, locale):
    # NB: jinja templates expect slashes, even on Windows
    tpl_path = os.path.join(FOLDER_PAGES, file_name).replace("\\", "/")
    translations_path = os.path.join(PATH_TO_TRANSLATIONS, file_name) + ".json"

    loader = jinja2.FileSystemLoader(searchpath=PATH_TO_SOURCES)
    env = jinja2.Environment(loader=loader, extensions=["jinja2.ext.i18n"])
    i18n = I18n(file_path=translations_path, locale=locale)
    env.install_gettext_translations(i18n, newstyle=True)

    return env.get_template(tpl_path).render({
        'i18n': i18n,
        'page': file_name,
    })


def build_page(file_name):
    for locale in LOCALES:
        contents = compile_template(file_name, locale)
        output_path = os.path.join(PATH_TO_PUBLISH, locale, file_name)
        ensure_directory_exists(output_path)
        with open(output_path, "w") as file:
            file.write(contents)


def copy_static_assets():
    shutil.copytree(PATH_TO_ASSETS, PATH_TO_PUBLISH, dirs_exist_ok=True)


def build_all():
    # Clear the publish folder
    shutil.rmtree(FOLDER_PUBLISH, ignore_errors=True)
    # Compile all pages
    for file_name in os.listdir(PATH_TO_PAGES):
        log(f"[build] Compiling {os.path.join(PATH_TO_PAGES, file_name)}...")
        build_page(file_name)
    # Copy non-templated assets
    copy_static_assets()
