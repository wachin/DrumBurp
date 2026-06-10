# Copyright 2026 Washington Indacochea Delgado
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
"""
DrumBurp internationalisation (i18n) loader.

Call install_translator(app) once, right after creating QApplication,
to load the correct .qm file for the current system locale.

Translation files live in src/i18n/ (development) or in the i18n/
subdirectory next to the frozen executable (PyInstaller builds):
    drumburp_en.qm
    drumburp_es.qm
    drumburp_de.qm
    drumburp_zh_TW.qm
    ...

To force a specific language at runtime (useful for testing):
    LANGUAGE=es ./run-drumburp.sh
or:
    python3 src/DrumBurp.py --language es
"""

import os
import sys
import xml.etree.ElementTree as ET
from PyQt5.QtCore import QTranslator, QCoreApplication, QLibraryInfo

# The translator instances — kept alive for the lifetime of the app.
_translator = None
_qt_translator = None


def _i18n_dir():
    """Return the directory that contains the .qm files.

    Works both in development (src/i18n/) and when frozen by PyInstaller
    (i18n/ next to the executable, bundled via --add-data).
    """
    if getattr(sys, 'frozen', False):
        # PyInstaller sets sys._MEIPASS to the temp extraction directory.
        return os.path.join(sys._MEIPASS, 'i18n')
    # Development: same directory as this file.
    return os.path.dirname(os.path.abspath(__file__))


def _translation_paths(language):
    """Return the candidate .qm and .ts paths for a language code."""
    base = os.path.join(_i18n_dir(), "drumburp_%s" % language)
    return base + ".qm", base + ".ts"


def _pick_translation(candidates):
    """Pick the best translation file for the requested candidates.

    Preference order:
    1. A newer .ts file (useful during development before running lrelease)
    2. A compiled .qm file
    3. A .ts file if no .qm exists
    """
    for candidate in candidates:
        qm_path, ts_path = _translation_paths(candidate)
        has_qm = os.path.exists(qm_path)
        has_ts = os.path.exists(ts_path)
        if has_ts and (not has_qm or
                       os.path.getmtime(ts_path) > os.path.getmtime(qm_path)):
            return candidate, "ts", ts_path
        if has_qm:
            return candidate, "qm", qm_path
        if has_ts:
            return candidate, "ts", ts_path
    return None, None, None


class _TsTranslator(QTranslator):
    """Minimal TS-file translator for development-time fallback."""

    def __init__(self, ts_path, parent=None):
        super().__init__(parent)
        self._messages = {}
        self._load_messages(ts_path)

    def _load_messages(self, ts_path):
        tree = ET.parse(ts_path)
        root = tree.getroot()
        for context in root.findall("context"):
            name = context.findtext("name") or ""
            if not name:
                continue
            for message in context.findall("message"):
                source = message.findtext("source") or ""
                translation = message.find("translation")
                if not source or translation is None:
                    continue
                text = translation.text or ""
                if not text:
                    continue
                self._messages[(name, source)] = text

    def isEmpty(self):
        return not self._messages

    def translate(self, context, sourceText, disambiguation=None, n=-1):
        return self._messages.get((context, sourceText), "")


def install_translator(app, language=None):
    """Load and install the translation for *language* (e.g. 'es', 'fr').

    If *language* is None the system locale is used.
    Falls back silently to the built-in English strings if no .qm file
    is found for the requested language.

    Returns the language code that was actually loaded, or None if the
    built-in English strings are being used.
    """
    global _translator

    if language is None:
        # Check environment variable first (useful for testing).
        language = os.environ.get("LANGUAGE") or os.environ.get("LANG", "")

    language = (language or "").strip()
    if not language:
        return None

    language = language.split(".")[0].replace("-", "_")
    if language.lower() == "en":
        return None  # English is the built-in language — nothing to load.

    candidates = [language]
    if "_" in language:
        base = language.split("_")[0]
        if base not in candidates:
            candidates.append(base)
    else:
        upper_language = language.lower()
        if upper_language not in candidates:
            candidates.append(upper_language)

    selected_language, translation_kind, translation_path = _pick_translation(
        candidates)
    if translation_path is None:
        return None  # No translation available — fall back to English.

    if translation_kind == "ts":
        _translator = _TsTranslator(translation_path, app)
        if _translator.isEmpty():
            return None
        QCoreApplication.installTranslator(_translator)
    else:
        _translator = QTranslator(app)
        if not _translator.load(translation_path):
            return None
        QCoreApplication.installTranslator(_translator)

    # Also load Qt's own built-in translation for standard widgets
    # (QDialogButtonBox buttons: OK, Cancel, etc.)
    global _qt_translator
    _qt_translator = QTranslator(app)
    qt_qm = QLibraryInfo.location(QLibraryInfo.TranslationsPath)
    qt_candidates = [selected_language]
    if "_" in selected_language:
        qt_candidates.append(selected_language.split("_")[0])
    for qt_language in qt_candidates:
        if _qt_translator.load("qtbase_" + qt_language, qt_qm):
            QCoreApplication.installTranslator(_qt_translator)
            break

    return selected_language
