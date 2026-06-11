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
Created on Mar 31, 2013

@author: Mike Thomas
'''

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog
from DBVersion import doesNewerVersionExist
from GUI.ui_versionDownloader import Ui_VersionDownloader


class QVersionDownloader(QDialog, Ui_VersionDownloader):
    def __init__(self, newer=None, parent=None):
        super(QVersionDownloader, self).__init__(parent=parent)
        self.setupUi(self)
        self._applyRichText()
        QTimer.singleShot(0, lambda: self._download(newer))

    def _linkColour(self):
        return self.palette().color(self.palette().Link).name()

    def _applyRichText(self):
        link_colour = self._linkColour()
        self.message.setOpenExternalLinks(True)
        self.resultLabel.setOpenExternalLinks(True)
        self.message.setText(
            "<html><head/><body><p><span style=\" font-size:8pt;\">"
            "Contacting </span><a href=\"http://www.whatang.org\">"
            "<span style=\" text-decoration: underline; color:%s;\">"
            "www.whatang.org</span></a><span style=\" font-size:8pt;\"> "
            "to detect latest version. Please wait...</span></p>"
            "</body></html>" % link_colour)

    def _download(self, newer):
        if newer is None:
            newer = doesNewerVersionExist()
        self.resultBox.setEnabled(True)
        self.message.setText(
            "Finished checking for new version at www.whatang.org.")
        if newer is None:
            self.resultLabel.setText('<span style="color:#ff0000;"><b>'
                                     'Failed :Could not access version information.'
                                     '</b></span>')
        elif newer == "":
            self.resultLabel.setText('<span style="color:#298018;">'
                                     'No newer version is available.'
                                     '<span>')
        else:
            newer = ".".join(str(v) for v in newer)
            self.resultLabel.setText('<span><b>'
                                     "DrumBurp version %s is now available "
                                     "from <a href='http://www.whatang.org'>"
                                     "<span style='text-decoration: underline; "
                                     "color:%s;'>www.whatang.org</span></a>"
                                     "</b></span>" %
                                     (newer, self._linkColour()))
