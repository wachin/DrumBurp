# Copyright 2026 Washington Indacochea Delgado
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
"""
Application theme helpers.
"""

import platform

from PyQt5.QtGui import QColor, QPalette

THEME_AUTO = "auto"
THEME_LIGHT = "light"
THEME_DARK = "dark"
THEME_MODES = (THEME_AUTO, THEME_LIGHT, THEME_DARK)


def normalise_theme_mode(mode):
    mode = (mode or "").strip().lower()
    if mode in THEME_MODES:
        return mode
    return THEME_AUTO


def _windows_apps_use_light_theme():
    try:
        import winreg
    except ImportError:
        return None
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize")
        try:
            value, unused_type = winreg.QueryValueEx(key, "AppsUseLightTheme")
            return bool(value)
        finally:
            winreg.CloseKey(key)
    except OSError:
        return None


def detect_system_dark_theme(app):
    if platform.system() == "Windows":
        uses_light = _windows_apps_use_light_theme()
        if uses_light is not None:
            return not uses_light
    window_colour = app.palette().color(QPalette.Window)
    return window_colour.lightness() < 128


def resolve_theme_mode(app, requested_mode):
    mode = normalise_theme_mode(requested_mode)
    if mode == THEME_DARK:
        return THEME_DARK
    if mode == THEME_LIGHT:
        return THEME_LIGHT
    if detect_system_dark_theme(app):
        return THEME_DARK
    return THEME_LIGHT


def _dark_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(45, 45, 48))
    palette.setColor(QPalette.WindowText, QColor(230, 230, 230))
    palette.setColor(QPalette.Base, QColor(30, 30, 30))
    palette.setColor(QPalette.AlternateBase, QColor(45, 45, 48))
    palette.setColor(QPalette.ToolTipBase, QColor(30, 30, 30))
    palette.setColor(QPalette.ToolTipText, QColor(230, 230, 230))
    palette.setColor(QPalette.Text, QColor(230, 230, 230))
    palette.setColor(QPalette.Button, QColor(60, 63, 65))
    palette.setColor(QPalette.ButtonText, QColor(230, 230, 230))
    palette.setColor(QPalette.BrightText, QColor(255, 85, 85))
    palette.setColor(QPalette.Link, QColor(86, 156, 214))
    palette.setColor(QPalette.Highlight, QColor(61, 109, 181))
    palette.setColor(QPalette.HighlightedText, QColor(255, 255, 255))
    palette.setColor(QPalette.Light, QColor(80, 80, 80))
    palette.setColor(QPalette.Midlight, QColor(70, 70, 70))
    palette.setColor(QPalette.Mid, QColor(55, 55, 55))
    palette.setColor(QPalette.Dark, QColor(35, 35, 35))
    palette.setColor(QPalette.Shadow, QColor(20, 20, 20))
    palette.setColor(QPalette.Disabled, QPalette.Text, QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.ButtonText,
                     QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.WindowText,
                     QColor(127, 127, 127))
    palette.setColor(QPalette.Disabled, QPalette.Highlight,
                     QColor(80, 80, 80))
    palette.setColor(QPalette.Disabled, QPalette.HighlightedText,
                     QColor(180, 180, 180))
    return palette


_DARK_STYLESHEET = """
QToolTip {
    color: #f0f0f0;
    background-color: #2d2d30;
    border: 1px solid #4f5357;
}
QMenu::separator {
    height: 1px;
    background: #4f5357;
    margin: 4px 8px;
}
QTabBar::tab:selected {
    background: #3d6db5;
    color: #ffffff;
}
QStatusBar {
    border-top: 1px solid #3a3d41;
}
"""


def apply_theme(app, requested_mode):
    actual_mode = resolve_theme_mode(app, requested_mode)
    if actual_mode == THEME_DARK:
        app.setStyle("Fusion")
        app.setPalette(_dark_palette())
        app.setStyleSheet(_DARK_STYLESHEET)
    else:
        app.setPalette(app.style().standardPalette())
        app.setStyleSheet("")
    app.setProperty("drumburpThemeMode", actual_mode)
    return actual_mode
