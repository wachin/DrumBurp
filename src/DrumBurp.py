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
Created on 31 Jul 2010

@author: Mike Thomas
'''
import sys
import argparse
from PyQt5.QtWidgets import QApplication
from DBVersion import APPNAME, DB_VERSION


def main():
    import ctypes
    from PyQt5.QtCore import QSettings
    parser = argparse.ArgumentParser()
    parser.add_argument('--virgin', action='store_true')
    parser.add_argument('--pyinstaller-test', action='store_true')
    parser.add_argument('--language', dest='language', default=None,
                        help='Force a specific UI language (e.g. es, fr, de)')
    parser.add_argument('filename', nargs='?')
    opts = parser.parse_args()
    if opts.pyinstaller_test:
        sys.exit(0)
    filename = opts.filename
    myappid = 'Whatang.DrumBurp'
    try:
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except AttributeError:
        pass
    app = QApplication(sys.argv)
    app.setOrganizationName("Whatang Software")
    app.setOrganizationDomain("whatang.org")
    app.setApplicationName(APPNAME)
    theme_mode = QSettings().value("ThemeMode", "auto", type=str)
    from GUI.DBTheme import apply_theme
    apply_theme(app, theme_mode)

    # Determine language: CLI flag > QSettings > LANGUAGE env var > system locale.
    # QSettings must be read after setOrganizationName/setApplicationName.
    language = opts.language
    if language is None:
        from PyQt5.QtCore import QSettings
        settings = QSettings()
        saved = settings.value("Language", "", type=str)
        if saved:
            language = saved  # use the language saved via the Help > Language menu

    # Install translation before any UI is created.
    from i18n.i18n import install_translator
    install_translator(app, language=language)
    import GUI.DBFonts
    import GUI.DBIcons
    import GUI.DBMainwindow
    import GUI.DBStartupDialog
    GUI.DBIcons.initialiseIcons()
    GUI.DBFonts.initialiseFonts()
    app.setWindowIcon(GUI.DBIcons.getIcon("drumburp"))
    startupSettings = QSettings()
    hideStartupDialog = startupSettings.value("HideStartupDialog", False,
                                              type=bool)
    if opts.virgin:
        hideStartupDialog = False
    if not hideStartupDialog:
        splash = GUI.DBStartupDialog.DBStartupDialog(DB_VERSION)
        splash.exec()
    mainWindow = GUI.DBMainwindow.DrumBurp(fakeStartup=opts.virgin,
                                           filename=filename)
    mainWindow.setWindowTitle("DrumBurp v" + DB_VERSION)
    mainWindow.show()
    app.exec()


if __name__ == '__main__':
    main()
