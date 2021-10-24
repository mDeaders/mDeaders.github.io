# Install

* Install [python](https://www.python.org/downloads/)
* Install python dependencies with `pip install -r requirements.txt`


# Devlopment

* Run local server with `python serve.py`
* Add / edit / remove files from `sources/
  (files in `docs/` are auto-generated)

## Templating

All HTML files may include templated code following the [JinJa2](https://jinja.palletsprojects.com/en/3.0.x/templates/) format.

## Translation

A simplified i18n system is embeded in the templating syntax:
* Use the `{% trans %}Hello world!{% endtrans %}` syntax to declare a translated text.
* You then need to add the translations in a related file under `sources/translations` (see current file for a format example - it's very simple).
* By default, the engine will try to load a translation file for each page by adding the `.json` extension to the page file
  Example: when building `pages/index.html`, it will automatically look for `translations/index.html.json`.
  There is no default loading for partials though !
* You can also add anotehr file with the template anotation `{% set _ = i18n.add_translation_file(FILE_NAME) -%}`.
  Example from `base.html`: `{% set _ = i18n.add_translation_file("base.html.json") -%}`
* For coherence purpose, you must provide translation for all supported locales. Else, the build will fail.


# Build

* Run `python build.py` to make sure published files are up to date.
  The files are created in the `docs/` folder which must be commited.

PS: no, you cannot change the `docs` name... #github

