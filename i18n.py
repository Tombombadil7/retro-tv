"""Gettext translations shared by Flask, Jinja and client-side JavaScript."""
import os
from flask import request
from flask_babel import Babel, get_domain

SUPPORTED_LANGUAGES = ("en", "he")


def select_locale():
    configured = os.environ.get("RETRO_TV_LANGUAGE", "").lower().replace("_", "-").split("-")[0]
    if configured in SUPPORTED_LANGUAGES:
        return configured
    return request.accept_languages.best_match(SUPPORTED_LANGUAGES) or "en"


def init_i18n(app):
    app.config["BABEL_DEFAULT_LOCALE"] = "en"
    app.config["BABEL_TRANSLATION_DIRECTORIES"] = "translations"
    Babel(app, locale_selector=select_locale)


def js_catalog():
    """Use compiled gettext translations; no duplicated JS key registry.

    Babel's catalog stores translated entries in _catalog (including a
    metadata entry and plural tuples), so only nonempty singular strings
    are sent to the browser.
    """
    catalog = get_domain().get_translations()._catalog
    return {key: value for key, value in catalog.items()
            if isinstance(key, str) and isinstance(value, str)
            and key and value and key != value}
