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
from GUI.ui_dbStartup import Ui_dbStartup
from PyQt5.QtCore import QSettings, Qt
from PyQt5.QtWidgets import QDialog


class DBStartupDialog(QDialog, Ui_dbStartup):
    def __init__(self, version, parent=None):
        super(DBStartupDialog, self).__init__(parent)
        self.setupUi(self)
        self._setWelcomeText()
        self.setWindowTitle(self.tr("Welcome to DrumBurp v") + version)
        self.buttonBox.button(self.buttonBox.Ok).setFocus()
        settings = QSettings()
        self.hideOnStartupCheckBox.setChecked(
            bool(settings.value("HideStartupDialog", False, type=bool)))

    def _linkColour(self):
        return self.palette().color(self.palette().Link).name()

    def _setWelcomeText(self):
        link_colour = self._linkColour()
        self.label.setTextFormat(Qt.RichText)
        self.label.setOpenExternalLinks(True)
        self.label.setWordWrap(True)
        self.label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        self.label.setText(
            '<html><head/><body>'
            '<p><span style=" font-size:10pt; font-weight:600; '
            'font-style:italic;">'
            + self.tr('DrumBurp Copyright (C) 2011-16 Michael Thomas')
            + '</span></p>'
            '<p><br/></p>'
            '<p>'
            + self.tr(
                'This program comes with ABSOLUTELY NO WARRANTY; for details '
                'see the <span style=" font-weight:600;">Help&gt;About '
                'DrumBurp</span> menu item. This is free software, and you '
                'are welcome to redistribute it under certain conditions; '
                'see the licensing information in <span style=" '
                'font-weight:600;">Help&gt;About DrumBurp</span> for details.')
            + '</p>'
            '<p><br/></p>'
            '<p>'
            + self.tr('Support and further licensing information is available at ')
            + '<a href="http://www.whatang.org">'
            + '<span style=" text-decoration: underline; color:%s;">'
            % link_colour
            + 'www.whatang.org</span></a>'
            + '</p></body></html>'
        )

    def accept(self):
        settings = QSettings()
        settings.setValue("HideStartupDialog",
                          self.hideOnStartupCheckBox.isChecked())
        settings.sync()
        super(DBStartupDialog, self).accept()
