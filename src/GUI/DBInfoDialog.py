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
Created on 17 Apr 2011

@author: Mike Thomas
'''

from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QDialog
from GUI import DBIcons
from GUI.ui_dbInfo import Ui_InfoDialog
from GUI.DBLicense import DBLicenseDialog


class DBInfoDialog(QDialog, Ui_InfoDialog):
    def __init__(self, version, parent=None):
        super(DBInfoDialog, self).__init__(parent)
        self.setupUi(self)
        self._applyThemeIcons()
        self.setWindowTitle(self.tr("DrumBurp v%s Information") % version)
        text = str(self.copyrightLabel.text())
        text += ' ' + self.tr("This is version %s.") % version
        self.copyrightLabel.setText(text)
        self._setContactDetailsText()
        self._setTechnologiesText()
        self._setLicenseText()
        self._addPortCredit()

    def _applyThemeIcons(self):
        self.label_2.setPixmap(DBIcons.buildIcon("drumburp.png").pixmap(48, 48))
        self.licenseButton.setIcon(DBIcons.buildIcon("gplv3-88x31.png"))
        self.licenseButton.setIconSize(QSize(44, 16))

    def _linkColour(self):
        return self.palette().color(self.palette().Link).name()

    def _setContactDetailsText(self):
        from PyQt5.QtCore import Qt
        link_colour = self._linkColour()
        self.label_3.setTextFormat(Qt.RichText)
        self.label_3.setOpenExternalLinks(True)
        self.label_3.setWordWrap(True)
        self.label_3.setText(
            '<p style="font-size:8pt;">'
            + self.tr('For more information go to ')
            + '<a href="http://www.whatang.org">'
            + '<span style="text-decoration: underline; color:%s;">'
            % link_colour
            + 'www.whatang.org</span></a>'
            + self.tr(' or email ')
            + '<a href="mailto:drumburp@whatang.org">'
            + '<span style="text-decoration: underline; color:%s;">'
            % link_colour
            + 'drumburp@whatang.org</span></a>.'
            + '</p>'
        )

    def _setTechnologiesText(self):
        """Set the Technologies label text so it is picked up by tr()."""
        from PyQt5.QtCore import Qt
        link_colour = self._linkColour()
        self.label_4.setTextFormat(Qt.RichText)
        self.label_4.setOpenExternalLinks(True)
        self.label_4.setWordWrap(True)
        self.label_4.setText(
            '<p style="font-size:8pt;">'
            + self.tr(
                'DrumBurp is built using ')
            + '<a href="http://www.python.org">'
            + '<span style="text-decoration: underline; color:%s;">Python</span></a> 3, '
            % link_colour
            + '<a href="http://www.riverbankcomputing.co.uk">'
            + '<span style="text-decoration: underline; color:%s;">PyQt</span></a> 5 '
            % link_colour
            + self.tr('and ')
            + '<a href="http://www.pygame.org">'
            + '<span style="text-decoration: underline; color:%s;">PyGame</span></a>.'
            % link_colour
            + '</p>'
        )

    def _setLicenseText(self):
        from PyQt5.QtCore import Qt
        link_colour = self._linkColour()
        self.label_5.setTextFormat(Qt.RichText)
        self.label_5.setOpenExternalLinks(True)
        self.label_5.setWordWrap(True)
        self.label_5.setText(
            '<p style="font-size:8pt;">'
            + self.tr('DrumBurp is issued under the ')
            + '<a href="http://www.gnu.org/licenses/gpl.html">'
            + '<span style="text-decoration: underline; color:%s;">GNU GPLv3</span></a>.'
            % link_colour
            + '</p>'
        )

    def _addPortCredit(self):
        from PyQt5.QtWidgets import QLabel, QSizePolicy
        from PyQt5.QtCore import Qt
        from PyQt5.QtGui import QFont

        bold = QFont()
        bold.setBold(True)

        label_title = QLabel(self.tr("PyQt4 -> PyQt5 Port"))
        label_title.setFont(bold)
        label_title.setAlignment(Qt.AlignCenter)

        label_info = QLabel(
            '<p style="font-size:8pt;">'
            + self.tr('Ported to Python 3 and PyQt5 by '
                      'Washington Indacochea Delgado ')
            + '(<a href="mailto:linuxfrontier@proton.me">'
            + '<span style="text-decoration: underline; color:%s;">'
            % self._linkColour()
            + 'linuxfrontier@proton.me</span></a>).'
            + '</p>'
        )
        label_info.setTextFormat(Qt.RichText)
        label_info.setOpenExternalLinks(True)
        label_info.setWordWrap(True)
        sp = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        label_info.setSizePolicy(sp)

        layout = self.gridLayout
        layout.removeWidget(self.buttonBox)
        layout.addWidget(label_title, 10, 0, 1, 1)
        layout.addWidget(label_info,  10, 2, 1, 1)
        layout.addWidget(self.buttonBox, 12, 0, 1, 3)

    @pyqtSlot()
    def on_licenseButton_clicked(self):  # IGNORE:R0201
        dlg = DBLicenseDialog(self)
        dlg.exec()
