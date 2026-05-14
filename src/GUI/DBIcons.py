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

import os

from PyQt5 import QtGui

_ICON_DIR = os.path.join(os.path.dirname(__file__), "Icons")

_ICON_CACHE = {"drumburp": "drumburp",
               "repeat": "view-refresh",
               "score": "audio-x-generic",
               "copy": "edit-copy",
               "paste": "edit-paste",
               "delete": "edit-delete"}


def initialiseIcons():
    for iconName, iconLocation in _ICON_CACHE.items():
        iconPath = os.path.join(_ICON_DIR, iconLocation + ".png")
        _ICON_CACHE[iconName] = QtGui.QIcon(iconPath)


def getIcon(iconName):
    return _ICON_CACHE[iconName.lower()]
