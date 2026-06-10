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


def _translation_path(language):
    """Return the candidate .qm path for a language code."""
    return os.path.join(_i18n_dir(), "drumburp_%s.qm" % language)


def _pick_translation(candidates):
    """Pick the first available compiled .qm translation."""
    for candidate in candidates:
        qm_path = _translation_path(candidate)
        if os.path.exists(qm_path):
            return candidate, qm_path
    return None, None


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

    selected_language, translation_path = _pick_translation(candidates)
    if translation_path is None:
        return None  # No translation available — fall back to English.

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
