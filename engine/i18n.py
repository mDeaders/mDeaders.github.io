from functools import lru_cache
import json
import os

from engine.constants import *
from engine.utils import log, InternalError


@lru_cache(maxsize=None)
def load_file(file_path):
    try:
        with open(file_path, "r") as file:
            contents = json.load(file)
        log(f"[i18n] Loaded {len(contents)} messages from {file_path} with their translations.")
        return contents
    except FileNotFoundError:
        log(f"[i18n] WARNING: Translation file \"{file_path}\" does not exist.")
        return []


class I18n:
    def __init__(self, file_path, locale="de"):
        self.locale = locale
        self.translations = load_file(file_path).copy()
        self.loaded_files = [file_path]

    def add_translation_file(self, file_name):
        file_path = os.path.join(PATH_TO_TRANSLATIONS, file_name)
        if file_path not in self.loaded_files:
            self.translations += load_file(file_path)
            self.loaded_files += file_path

    def find(self, message, locale):
        for translation in self.translations:
            if translation.get(locale) == message:
                return translation
        raise InternalError(f"[i18n] No translation found for message \"{message}\".")

    def gettext(self, message):
        translations = self.find(message, "de")
        return translations.get(self.locale)

    def ugettext(self, message):
        translations = self.find(message, "de")
        return translations.get(self.locale)

    def ngettext(self, singular, plural, n):
        print(f"ngettext({singular}, {plural}, {n})", flush=True)
        raise RuntimeError("ngettext() is not implemented")

    def ungettext(self, singular, plural, n):
        print(f"ungettext({singular}, {plural}, {n})", flush=True)
        raise RuntimeError("ungettext() is not implemented")
