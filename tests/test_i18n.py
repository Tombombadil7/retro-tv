"""Basic localization integration checks."""
import os
import unittest
from unittest.mock import patch
from pathlib import Path
from flask import Flask, render_template
from flask_babel import get_locale
from i18n import init_i18n, js_catalog


class I18nTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__, template_folder=str(Path(__file__).resolve().parents[1] / "templates"))
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

    def render_base(self, language):
        with patch.dict(os.environ, {"RETRO_TV_LANGUAGE": language}):
            with self.app.test_request_context("/"):
                return render_template(
                    "base.html",
                    current_language=str(get_locale()),
                    js_translations=js_catalog(),
                    config_timezone="America/New_York",
                )

    def test_english_template_keeps_ltr_and_navigation(self):
        html = self.render_base("en")
        self.assertIn('<html lang="en" dir="ltr">', html)
        self.assertIn('>TV Guide</a>', html)
        self.assertIn('>Sports</a>', html)
        self.assertIn('window.TV_TRANSLATIONS=', html)

    def test_hebrew_template_sets_rtl(self):
        html = self.render_base("he")
        self.assertIn('<html lang="he" dir="rtl">', html)
        self.assertIn('window.TV_LANGUAGE="he"', html)

    def test_js_catalog(self):
        with self.app.test_request_context("/"):
            self.assertIsInstance(js_catalog(), dict)


if __name__ == "__main__":
    unittest.main()
