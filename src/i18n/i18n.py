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
    ...

To force a specific language at runtime (useful for testing):
    LANGUAGE=es ./run-drumburp.sh
or:
    python3 src/DrumBurp.py --language es
"""

import os
import sys
from PyQt5.QtCore import QTranslator, QCoreApplication

# The single translator instance — kept alive for the lifetime of the app.
_translator = None


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
        # Keep only the language part: "es_AR.UTF-8" -> "es"
        language = language.split("_")[0].split(".")[0].lower()

    if not language or language == "en":
        return None  # English is the built-in language — nothing to load.

    qm_path = os.path.join(_i18n_dir(), "drumburp_%s.qm" % language)
    if not os.path.exists(qm_path):
        return None  # No translation available — fall back to English.

    _translator = QTranslator(app)
    if _translator.load(qm_path):
        QCoreApplication.installTranslator(_translator)
        return language

    return None
