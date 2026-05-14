# Copyright 2015 Michael Thomas
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
Created on Jul 19, 2015

@author: Mike Thomas
'''

import os

from PyQt5.QtGui import QFontDatabase, QFont
import Data.FontOptions

_FONT_DIR = os.path.join(os.path.dirname(__file__), "fonts")


def initialiseFonts():
    fonts = [("NotCourierSans", "NotCourierSans.otf"),
             ("Inconsolata", "Inconsolata.otf"),
             ("BPmono", "BPmono.ttf"),
             ("Liberation Mono", "LiberationMono-Regular.ttf"),
             ("Oxygen Mono", "OxygenMono-Regular.otf"),
             ("Open Sans", "OpenSans-Regular.ttf"),
             ("Montserrat", "Montserrat-Regular.ttf"),
             ("Noto Sans", "NotoSans-Regular.ttf"),
             ("PT Sans", "PT_Sans-Web-Regular.ttf"),
             ("Raleway", "Raleway-Regular.ttf"),
             ("Roboto", "Roboto-Regular.ttf")]
    for fontName, fontFile in fonts:
        fontPath = os.path.join(_FONT_DIR, fontFile)
        if QFontDatabase.addApplicationFont(fontPath) == -1:
            print(fontName)
        else:
            font = QFont(fontName)
            Data.FontOptions.FontOptions.addFont(fontName, font)
