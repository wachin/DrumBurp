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

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from GUI.ui_dbInfo import Ui_InfoDialog
from GUI.DBLicense import DBLicenseDialog


class DBInfoDialog(QDialog, Ui_InfoDialog):
    def __init__(self, version, parent=None):
        super(DBInfoDialog, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle(self.tr("DrumBurp v%s Information") % version)
        text = str(self.copyrightLabel.text())
        text += ' ' + self.tr("This is version %s.") % version
        self.copyrightLabel.setText(text)
        self._setTechnologiesText()
        self._addPortCredit()

    def _setTechnologiesText(self):
        """Set the Technologies label text so it is picked up by tr()."""
        from PyQt5.QtCore import Qt
        self.label_4.setTextFormat(Qt.RichText)
        self.label_4.setOpenExternalLinks(True)
        self.label_4.setWordWrap(True)
        self.label_4.setText(
            '<p style="font-size:8pt;">'
            + self.tr(
                'DrumBurp is built using '
                '<a href="http://www.python.org">Python</a> 3, '
                '<a href="http://www.riverbankcomputing.co.uk">PyQt</a> 5 '
                'and <a href="http://www.pygame.org">PyGame</a>.')
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
                      'Washington Indacochea Delgado '
                      '(<a href="mailto:linuxfrontier@proton.me">'
                      'linuxfrontier@proton.me</a>).')
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
