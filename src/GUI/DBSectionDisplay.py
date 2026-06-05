# Copyright 2026 Washington Indacochea Delgado
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

import re

from PyQt5.QtCore import QCoreApplication


_STANDARD_SECTION_TITLE = re.compile(
    r"^(Intro|Verse|Chorus|Bridge|Outro)(\s+\d+)?$")


def displaySectionTitle(title):
    match = _STANDARD_SECTION_TITLE.match(title)
    if match is None:
        return title
    stem, suffix = match.groups()
    translatedStems = {
        "Intro": QCoreApplication.translate("DrumBurp", "Intro"),
        "Verse": QCoreApplication.translate("DrumBurp", "Verse"),
        "Chorus": QCoreApplication.translate("DrumBurp", "Chorus"),
        "Bridge": QCoreApplication.translate("DrumBurp", "Bridge"),
        "Outro": QCoreApplication.translate("DrumBurp", "Outro"),
    }
    translatedTitle = translatedStems[stem] + (suffix or "")
    if translatedTitle == title:
        return title
    return "%s (%s)" % (title, translatedTitle)
