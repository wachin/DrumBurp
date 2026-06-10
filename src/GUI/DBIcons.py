# Copyright 2011-12 Michael Thomas
#
# See www.whatang.org for more information.
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# DrumBurp is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with DrumBurp.  If not, see <http://www.gnu.org/licenses/>
'''
Created on 23 Jan 2011

@author: Mike Thomas
'''

from PyQt5 import QtCore, QtGui, QtWidgets

from GUI.DBTheme import THEME_DARK, THEME_LIGHT

_ICON_RESOURCE_PREFIX = ":/Icons/Icons"
_DARK_ICON_RESOURCE_PREFIX = ":/Icons/Icons/dark"

_ICON_NAME_MAP = {"drumburp": "drumburp.png",
                  "repeat": "view-refresh.png",
                  "score": "audio-x-generic.png",
                  "copy": "edit-copy.png",
                  "paste": "edit-paste.png",
                  "delete": "edit-delete.png"}

_ICON_CACHE = {}


def _currentThemeMode():
    app = QtWidgets.QApplication.instance()
    if app is None:
        return THEME_LIGHT
    return app.property("drumburpThemeMode") or THEME_LIGHT


def _resourcePath(filename, theme_mode):
    if theme_mode == THEME_DARK:
        dark_path = "%s/%s" % (_DARK_ICON_RESOURCE_PREFIX, filename)
        if QtCore.QFile.exists(dark_path):
            return dark_path
    return "%s/%s" % (_ICON_RESOURCE_PREFIX, filename)


def _cacheKey(off_filename, on_filename, theme_mode):
    return (off_filename, on_filename, theme_mode)


def initialiseIcons():
    _ICON_CACHE.clear()


def buildIcon(off_filename, on_filename=None, theme_mode=None):
    app = QtWidgets.QApplication.instance()
    if app is None:
        return QtGui.QIcon()
    theme_mode = theme_mode or _currentThemeMode()
    key = _cacheKey(off_filename, on_filename, theme_mode)
    if key in _ICON_CACHE:
        return _ICON_CACHE[key]
    icon = QtGui.QIcon(_resourcePath(off_filename, theme_mode))
    if on_filename is not None:
        icon.addFile(_resourcePath(on_filename, theme_mode),
                     state=QtGui.QIcon.On)
    _ICON_CACHE[key] = icon
    return icon


def getIcon(iconName, theme_mode=None):
    return buildIcon(_ICON_NAME_MAP[iconName.lower()], theme_mode=theme_mode)
