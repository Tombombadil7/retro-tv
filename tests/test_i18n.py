"""Basic localization integration checks."""
import os
import unittest
from unittest.mock import patch
from flask import Flask
from flask_babel import get_locale
from i18n import init_i18n, js_catalog


class I18nTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        init_i18n(self.app)

    def test_default_language(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.app.test_request_context("/", headers={"Accept-Language": "fr"}):
                self.assertEqual(str(get_locale()), "en")

    def test_browser_language(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.app.test_request_context("/", headers={"Accept-Language": "he-IL,he;q=0.9,en;q=0.5"}):
                self.assertEqual(str(get_locale()), "he")

    def test_forced_language(self):
        with patch.dict(os.environ, {"RETRO_TV_LANGUAGE": "he-IL"}):
            with self.app.test_request_context("/"):
                self.assertEqual(str(get_locale()), "he")

    def test_js_catalog(self):
        with self.app.test_request_context("/"):
            self.assertIsInstance(js_catalog(), dict)


if __name__ == "__main__":
    unittest.main()
