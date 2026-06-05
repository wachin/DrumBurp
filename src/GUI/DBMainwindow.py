# Copyright 2011-2012 Michael Thomas
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
from io import BytesIO, StringIO
import os
import re
import shutil
import webbrowser

from PyQt5.QtCore import QSettings, QTimer, QThread, pyqtSignal, pyqtSlot, Qt, \
    QStandardPaths, QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtPrintSupport import QPrintPreviewDialog, QPrinterInfo, QPrinter
from PyQt5.QtWidgets import (QMainWindow, QFileDialog, QMessageBox,
                             QWhatsThis, QLabel, QFrame, QAction, QActionGroup)

from DBVersion import APPNAME, DB_VERSION, doesNewerVersionExist
from Data import FontOptions
from Data.DBConstants import CURRENT_FILE_FORMAT
from Data.DBErrors import InconsistentRepeats
from GUI.DBFSMEvents import StartPlaying, StopPlaying
from GUI.DBInfoDialog import DBInfoDialog
from GUI.LilypondExporter import LilypondExporter
from GUI.QDisplayProperties import QDisplayProperties
from GUI.QEditMeasureDialog import QEditMeasureDialog
from GUI.QLilypondPreview import QLilypondPreview
from GUI.QNewScoreDialog import QNewScoreDialog
from GUI.QScore import QScore
from GUI.QVersionDownloader import QVersionDownloader
from GUI.ui_drumburp import Ui_DrumBurpWindow
from Notation import AsciiExport
from Notation.lilypond import LilypondScore, LilypondProblem, findLilyPath
import GUI.DBColourPicker as DBColourPicker
import GUI.DBIcons as DBIcons
import GUI.DBMidi as DBMidi


# pylint:disable=too-many-instance-attributes,too-many-public-methods


def _dialogFilename(result):
    if isinstance(result, tuple):
        return result[0]
    return result


def _homeLocation():
    return (QStandardPaths.writableLocation(QStandardPaths.HomeLocation)
            or os.path.expanduser("~"))


_STANDARD_SECTION_TITLE = re.compile(
    r"^(Intro|Verse|Chorus|Bridge|Outro)(\s+\d+)?$")


def _displaySectionTitle(title):
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
    translatedStem = translatedStems[stem]
    translatedTitle = translatedStem + (suffix or "")
    if translatedTitle == title:
        return title
    return "%s (%s)" % (title, translatedTitle)


def _settingsValue(settings, key, default=None, valueType=None):
    try:
        if valueType is None:
            value = settings.value(key, default)
        else:
            value = settings.value(key, default, type=valueType)
    except (TypeError, RuntimeError, SystemError):
        try:
            value = settings.value(key, default)
        except (TypeError, RuntimeError, SystemError):
            return default
    if value is None:
        return default
    if valueType is str:
        if hasattr(value, "toString"):
            return value.toString()
        if isinstance(value, bytes):
            return value.decode("utf-8", "replace")
        return str(value)
    if valueType is bool:
        if hasattr(value, "toBool"):
            return value.toBool()
        if isinstance(value, str):
            return value.lower() in ("1", "true", "yes", "on")
        return bool(value)
    if valueType is list:
        if hasattr(value, "toStringList"):
            return value.toStringList()
        if isinstance(value, (list, tuple)):
            return list(value)
        return default
    return value


def _normalisePath(path):
    if path is None:
        return None
    if isinstance(path, bytes):
        return path.decode("utf-8", "replace")
    path = str(path)
    if ((path.startswith("b'") and path.endswith("'")) or
            (path.startswith('b"') and path.endswith('"'))):
        return path[2:-1]
    return path


_SCORE_EXTENSIONS = (".brp",)


def _isScoreFilename(filename):
    if filename is None:
        return False
    return os.path.splitext(str(filename))[1].lower() in _SCORE_EXTENSIONS


def _scoreFileFilter(parent):
    return parent.tr("DrumBurp files (*.brp)")


class FakeQSettings(object):
    def value(self, key_, default=None, type=None):  # IGNORE:no-self-use,redefined-builtin
        return default

    def setValue(self, key_, value_):  # IGNORE:no-self-use
        return

    def contains(self, key_):
        return False

    def sync(self):
        return


class DrumBurp(QMainWindow, Ui_DrumBurpWindow):
    exporterDone = pyqtSignal(str)

    def __init__(self, parent=None, fakeStartup=False, filename=None):
        self._fakeStartup = fakeStartup
        super(DrumBurp, self).__init__(parent)
        self._state = None
        self._asciiSettings = None
        self._printer = None
        self._midiPlaybackEnabled = False
        self.setupUi(self)
        self.scoreScene = None
        self.paperBox.blockSignals(True)
        self.paperBox.clear()
        self._knownPageHeights = []
        self._exporter = None
        self.lilyPath = None
        self.colourScheme = DBColourPicker.ColourScheme()
        printer = QPrinter()
        printer.setOutputFileName("invalid.pdf")
        for name in dir(QPrinter):
            attr = getattr(QPrinter, name)
            if (isinstance(attr, QPrinter.PageSize)
                    and name != "Custom"):
                self.paperBox.addItem(name)
                printer.setPaperSize(attr)
                self._knownPageHeights.append(printer.pageRect().height())
        self._pageHeight = printer.paperRect().height()
        self.paperBox.blockSignals(False)
        settings = self._makeQSettings()
        self.lilyPath = _normalisePath(
            _settingsValue(settings, "LilypondPath", "", str))
        if not self.lilyPath or not os.path.exists(self.lilyPath):
            self.lilyPath = _normalisePath(findLilyPath())
        self.lastScoreDirectory = _normalisePath(
            _settingsValue(settings, "LastScoreDirectory", "", str))
        if (not self.lastScoreDirectory or
                not os.path.isdir(self.lastScoreDirectory)):
            self.lastScoreDirectory = None
        recentFiles = _settingsValue(settings, "RecentFiles", [], list) or []
        self.recentFiles = [str(fname) for fname in recentFiles
                            if (_isScoreFilename(fname) and
                                os.path.exists(str(fname)))]
        if filename is not None and not _isScoreFilename(filename):
            filename = None
        if filename is None:
            filename = (None
                        if len(self.recentFiles) == 0
                        else self.recentFiles[0])
        self.filename = filename
        self.addToRecentFiles()
        self.updateRecentFiles()
        self.songProperties = QDisplayProperties()
        self._lilyScene = QLilypondPreview(self)
        self.lilyPreview.setScene(self._lilyScene)
        # Fonts
        fonts = list(FontOptions.FontOptions.iterAllowedFonts())
        fonts.sort()
        for index, (fontName, font) in enumerate(fonts):
            for combo in (self.noteFontComboBox, self.sectionFontCombo,
                          self.metadataFontCombo):
                combo.addItem(fontName)
                combo.setItemData(index, font, Qt.FontRole)
        # Create scene
        erroredFiles = []
        oldFilename = self.filename
        self.scoreScene = QScore(self)
        if oldFilename is not None and self.filename is None:
            erroredFiles.append(oldFilename)
            try:
                self.recentFiles.remove(self.filename)
            except ValueError:
                pass
        geometry = _settingsValue(settings, "Geometry")
        if geometry:
            self.restoreGeometry(geometry)
        windowState = _settingsValue(settings, "MainWindow/State")
        if windowState:
            self.restoreState(windowState)
        self._readColours(settings)
        self.statusbar.addPermanentWidget(QFrame())
        self.availableNotesLabel = QLabel()
        self.availableNotesLabel.setMinimumWidth(250)
        self.statusbar.addPermanentWidget(self.availableNotesLabel)
        self._infoBar = QLabel()
        self.statusbar.addPermanentWidget(self._infoBar)
        self._initializeState()
        self._buildLanguageMenu()
        self.setSections()
        self._versionThread = VersionCheckThread()
        self._versionThread.finished.connect(self._finishedVersionCheck)
        self.menuSelectMidiOut.setEnabled(False)
        self.menuSelectMidiOut.menuAction().setVisible(True)
        self.setAcceptDrops(True)
        self._midiInitThread = DBMidi.MidiInit(self)
        self._midiInitThread.finished.connect(self._midiInitFinished)
        QTimer.singleShot(0, lambda: self._startUp(erroredFiles))
        self.actionCheckOnStartup.setChecked(
            _settingsValue(settings, "CheckOnStartup", False, bool))
        self.statusbar.showMessage(self.tr("Initializing MIDI..."))
        self.setEnabled(False)

    def _connectSignals(self, props, scene):
        # Connect signals
        props.fontChanged.connect(self._setNoteFont)
        props.noteSizeChanged.connect(self.noteSizeSpinBox.setValue)
        props.sectionFontChanged.connect(self._setSectionFont)
        props.sectionFontSizeChanged.connect(self._setSectionFontSize)
        props.metadataFontChanged.connect(self._setMetadataFont)
        props.metadataFontSizeChanged.connect(self._setMetadataSize)
        scene.dirtySignal.connect(self.setWindowModified)
        scene.dragHighlight.connect(self._setMidiSelectionActionsEnabled)
        scene.dragHighlight.connect(self.actionCopyMeasures.setEnabled)
        scene.dragHighlight.connect(self.checkPasteMeasure)
        scene.dragHighlight.connect(self.actionClearMeasures.setEnabled)
        scene.dragHighlight.connect(self.actionDeleteMeasures.setEnabled)
        scene.sceneFormatted.connect(self.sceneFormatted)
        scene.playing.connect(self._scorePlaying)
        scene.currentHeadsChanged.connect(self.availableNotesLabel.setText)
        scene.statusMessageSet.connect(self._setStatusFromScene)
        scene.lilysizeChanged.connect(self._setLilySize)
        scene.lilypagesChanged.connect(self._setLilyPages)
        scene.lilyFillChanged.connect(self._setLilyFill)
        scene.lilyFormatChanged.connect(self._setLilyFormat)
        scene.showItem.connect(self.scoreView.showItemAtTop)
        scene.widthChanged.connect(self.scoreView.setWidth)
        self.paperBox.currentIndexChanged[int].connect(self._setPaperSize)
        props.kitDataVisibleChanged.connect(self._setKitDataVisible)
        props.emptyLinesVisibleChanged.connect(self._setEmptyLinesVisible)
        props.measureCountsVisibleChanged.connect(
            self._setMeasureCountsVisible)
        props.metadataVisibilityChanged.connect(self._setMetadataVisible)
        props.beatCountVisibleChanged.connect(self._setBeatCountVisible)
        DBMidi.SONGEND_SIGNAL.connect(self.musicDone)
        DBMidi.HIGHLIGHT_SIGNAL.connect(self.highlightPlayingMeasure)
        self.exporterDone.connect(self._finishLilyExport)
        self.refreshLilypond.clicked.connect(self._lilyScene.preview)
        self.scoreScene.scoreDisplayChanged.connect(self._refreshTextExport)
        self.underlineCheck.clicked.connect(self._refreshTextExport)
        self.sectionBracketsCheck.clicked.connect(self._refreshTextExport)
        self.emptyLineBeforeSectionCheck.clicked.connect(
            self._refreshTextExport)
        self.emptyLineAfterSectionCheck.clicked.connect(
            self._refreshTextExport)
        self.noteFontComboBox.currentIndexChanged[int].connect(
            self._noteFontChanged)
        self.metadataFontCombo.currentIndexChanged[int].connect(
            self._metadataFontChanged)
        self.sectionFontCombo.currentIndexChanged[int].connect(
            self._sectionFontChanged)

    def _initializeState(self):
        props = self.songProperties
        scene = self.scoreScene
        self.scoreView.setScene(scene)
        self._connectSignals(props, scene)
        self.lineSpaceSlider.setValue(scene.systemSpacing)
        # Fonts
        self._setNoteFont()
        self.noteSizeSpinBox.setValue(props.noteFontSize)
        self._setSectionFont()
        self.sectionFontSizeSpinbox.setValue(props.sectionFontSize)
        self._setMetadataFont()
        self.metadataFontSizeSpinbox.setValue(props.metadataFontSize)
        # Visibility toggles
        self.actionShowDrumKey.setChecked(props.kitDataVisible)
        self.actionShowEmptyLines.setChecked(props.emptyLinesVisible)
        self.actionShowScoreInfo.setChecked(props.metadataVisible)
        self.actionShowBeatCount.setChecked(props.beatCountVisible)
        self.actionShowMeasureCounts.setChecked(props.measureCountsVisible)
        # Set doable actions
        self.actionPlayOnce.setEnabled(False)
        self.actionLoopBars.setEnabled(False)
        self.actionCopyMeasures.setEnabled(False)
        self.actionPasteMeasures.setEnabled(False)
        self.actionFillPasteMeasures.setEnabled(False)
        self.actionClearMeasures.setEnabled(False)
        self.actionDeleteMeasures.setEnabled(False)
        self.menu_MIDI.setEnabled(True)
        self.MIDIToolBar.setEnabled(True)
        self._setMidiPlaybackEnabled(False)
        # Undo/redo
        self.actionUndo.setEnabled(False)
        self.actionRedo.setEnabled(False)
        scene.canUndoChanged.connect(self.actionUndo.setEnabled)

        def changeUndoText(txt): return self.actionUndo.setText(self.tr("Undo %s") % txt)
        scene.undoTextChanged.connect(changeUndoText)
        scene.canRedoChanged.connect(self.actionRedo.setEnabled)

        def changeRedoText(txt): return self.actionRedo.setText(self.tr("Redo %s") % txt)
        scene.redoTextChanged.connect(changeRedoText)
        # Default beat
        self._beatChanged(scene.defaultCount)
        self.widthSpinBox.setValue(scene.scoreWidth)
        # Default Lilypond settings
        self.lilypondSize.setValue(scene.score.lilysize)
        self.lilyPagesBox.setValue(scene.score.lilypages)
        self.lilyFillButton.setChecked(scene.score.lilyFill)
        self._setLilyFormat(scene.score.lilyFormat)
        self.prevLilyPage.clicked.connect(self._lilyScene.previousPage)
        self.nextLilyPage.clicked.connect(self._lilyScene.nextPage)
        self.firstLilyPage.clicked.connect(self._lilyScene.firstPage)
        self.lastLilyPage.clicked.connect(self._lilyScene.lastPage)

    def _startUp(self, erroredFiles):
        self._midiInitThread.start()
        self._doUpdateSplashScreen()
        self.scoreView.startUp()
        self.updateStatus(self.tr("Welcome to %s v%s") % (APPNAME, DB_VERSION))
        self.scoreView.setFocus()
        if self.actionCheckOnStartup.isChecked():
            #             self.on_actionCheckForUpdates_triggered()
            self._versionThread.start()
        if erroredFiles:
            QMessageBox.warning(self, self.tr("Problem during startup"),
                                self.tr("Error opening files:\n %s") %
                                "\n".join(erroredFiles))

    def _doUpdateSplashScreen(self):
        settings = self._makeQSettings()
        if _settingsValue(settings, "NoUpdateSplash", False, bool):
            return
        splashUpdates = QMessageBox(self)
        splashUpdates.setStandardButtons(QMessageBox.Ok)
        splashUpdates.setText(self.tr("<b>DrumBurp can check for updates.</b>"))
        text = self.tr(
            "DrumBurp can automatically check for updates every time it "
            "starts, or you can manually check for a new version. Both "
            "options are available from the Help menu.\n\nWhen DrumBurp "
            "tries to check for an update it will try to access the "
            "internet. You may need to allow it access in order for the "
            "update check to work.")
        splashUpdates.setInformativeText(text)
        splashUpdates.setDefaultButton(QMessageBox.Ok)
        splashUpdates.setEscapeButton(QMessageBox.Ok)
        neverAgain = splashUpdates.addButton(self.tr("Do not show this again"),
                                             QMessageBox.ActionRole)
        splashUpdates.setWindowTitle(self.tr("Update Checks"))
        splashUpdates.exec()
        if splashUpdates.clickedButton() == neverAgain:
            settings.setValue("NoUpdateSplash", True)
            settings.sync()

    def _makeQSettings(self):
        if self._fakeStartup:
            return FakeQSettings()
        else:
            return QSettings()

    def _setPaperSize(self, unusedIndex):
        self.scoreScene.setPaperSize(self.paperBox.currentText())

    def _setMidiPlaybackEnabled(self, enabled):
        self._midiPlaybackEnabled = enabled
        self.actionPlayScore.setEnabled(enabled)
        self.actionMuteNotes.setEnabled(enabled)
        self._setMidiSelectionActionsEnabled(
            self.scoreScene is not None and self.scoreScene.hasDragSelection())

    def _setMidiSelectionActionsEnabled(self, hasSelection):
        enabled = self._midiPlaybackEnabled and hasSelection
        self.actionPlayOnce.setEnabled(enabled)
        self.actionLoopBars.setEnabled(enabled)

    def _setFontCombo(self, font, fontCombo):
        if font is None:
            fontName = FontOptions.FontOptions.DEFAULT_FONT
        else:
            fontName = font.family()
        index = fontCombo.findText(fontName)
        if index == -1:
            index = 0
        fontCombo.setCurrentIndex(index)

    def _setNoteFont(self):
        self._setFontCombo(self.songProperties.noteFont, self.noteFontComboBox)

    def _noteFontChanged(self, index_):
        fontName = self.noteFontComboBox.currentText()
        font = QFont(fontName)
        font.setPointSize(self.noteSizeSpinBox.value())
        self.scoreView.scene().setScoreFont(font, "note")

    def _setNoteFontSize(self):
        props = self.songProperties
        self.noteSizeSpinBox.setValue(props.noteFontSize)

    def _setSectionFont(self):
        self._setFontCombo(self.songProperties.sectionFont,
                           self.sectionFontCombo)

    def _sectionFontChanged(self, index_):
        fontName = self.sectionFontCombo.currentText()
        font = QFont(fontName)
        font.setPointSize(self.sectionFontSizeSpinbox.value())
        self.scoreView.scene().setScoreFont(font, "section")

    def _setSectionFontSize(self):
        props = self.songProperties
        self.sectionFontSizeSpinbox.setValue(props.sectionFontSize)

    def _setMetadataFont(self):
        self._setFontCombo(self.songProperties.metadataFont,
                           self.metadataFontCombo)

    def _metadataFontChanged(self, index_):
        fontName = self.metadataFontCombo.currentText()
        font = QFont(fontName)
        font.setPointSize(self.metadataFontSizeSpinbox.value())
        self.scoreView.scene().setScoreFont(font, "metadata")

    def _setMetadataSize(self):
        props = self.songProperties
        self.metadataFontSizeSpinbox.setValue(props.metadataFontSize)

    def _setKitDataVisible(self):
        props = self.songProperties
        if props.kitDataVisible != self.actionShowDrumKey.isChecked():
            self.actionShowDrumKey.setChecked(props.kitDataVisible)

    def _setMetadataVisible(self):
        props = self.songProperties
        if props.metadataVisible != self.actionShowScoreInfo.isChecked():
            self.actionShowScoreInfo.setChecked(props.metadataVisible)

    def _setEmptyLinesVisible(self):
        props = self.songProperties
        if props.emptyLinesVisible != self.actionShowEmptyLines.isChecked():
            self.actionShowEmptyLines.setChecked(props.emptyLinesVisible)

    def _setBeatCountVisible(self):
        props = self.songProperties
        if props.beatCountVisible != self.actionShowBeatCount.isChecked():
            self.actionShowBeatCount.setChecked(props.beatCountVisible)

    def _setMeasureCountsVisible(self):
        props = self.songProperties
        if (props.measureCountsVisible !=
                self.actionShowMeasureCounts.isChecked()):
            self.actionShowMeasureCounts.setChecked(props.measureCountsVisible)

    def updateStatus(self, message):
        self.statusBar().showMessage(message, 5000)
        if self.filename is not None:
            self.setWindowTitle(self.tr("DrumBurp v%s - %s[*]")
                                % (DB_VERSION, os.path.basename(self.filename)))
        else:
            self.setWindowTitle(self.tr("DrumBurp v%s - Untitled[*]") % DB_VERSION)
        self.setWindowModified(self.scoreScene.dirty)

    def okToContinue(self):
        if self.scoreScene.dirty:
            reply = QMessageBox.question(
                self,
                self.tr("DrumBurp - Unsaved Changes"),
                self.tr("Save unsaved changes?"),
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Cancel)
            if reply == QMessageBox.Cancel:
                return False
            elif reply == QMessageBox.Yes:
                if not self.fileSave():
                    msg = self.tr(
                        "DrumBurp could not save the file."
                        "\n\n"
                        "Continue anyway? "
                        "All unsaved changes will be lost!")
                    failReply = QMessageBox.warning(self,
                                                    self.tr("Failed Save!"),
                                                    msg,
                                                    QMessageBox.Yes | QMessageBox.No,
                                                    QMessageBox.No)
                    return failReply == QMessageBox.Yes
        return True

    def closeEvent(self, event):
        if self.okToContinue():
            settings = self._makeQSettings()
            settings.setValue("RecentFiles", self.recentFiles)
            settings.setValue("LastScoreDirectory",
                              self.lastScoreDirectory or _homeLocation())
            settings.setValue("Geometry", self.saveGeometry())
            settings.setValue("MainWindow/State", self.saveState())
            settings.setValue("CheckOnStartup",
                              self.actionCheckOnStartup.isChecked())
            settings.setValue("LilypondPath", self.lilyPath)
            self._writeColours(settings)
            self.songProperties.save(settings)
            self._versionThread.exit()
            self._versionThread.wait(1000)
            if not self._versionThread.isFinished():
                self._versionThread.terminate()
            self._midiInitThread.exit()
            self._midiInitThread.wait(1000)
            if not self._midiInitThread.isFinished():
                self._midiInitThread.terminate()
            if self._exporter is not None:
                self._exporter.exit()
                self._exporter.wait(1000)
                if not self._exporter.isFinished():
                    self._exporter.terminate()
            self._lilyScene.cleanup()
        else:
            event.ignore()

    def _writeColours(self, settings):
        for colour in self.colourScheme.iterColours():
            colourRef = colour.colourAttrs.attrName
            settings.setValue("Colours/" + colourRef, colour.toString())

    def _readColours(self, settings):
        for colour in self.colourScheme.iterColours():
            colourRef = colour.colourAttrs.attrName
            if not settings.contains("Colours/" + colourRef):
                continue
            col = _settingsValue(settings, "Colours/" + colourRef, "", str)
            colour.fromString(col)

    @pyqtSlot()
    def on_actionFitInWindow_triggered(self):
        widthInPixels = self.scoreView.width()
        maxColumns = self.songProperties.maxColumns(widthInPixels)
        self.widthSpinBox.setValue(maxColumns)
        self.scoreScene.reBuild()

    @pyqtSlot()
    def on_actionLoad_triggered(self):
        if not self.okToContinue():
            return
        caption = self.tr("Choose a DrumBurp file to open")
        directory = self._scoreDialogDirectory()
        fname = QFileDialog.getOpenFileName(parent=self,
                                            caption=caption,
                                            directory=directory,
                                            filter=_scoreFileFilter(self))
        fname = _dialogFilename(fname)
        if len(fname) == 0:
            return
        self._loadScore(fname)

    def _loadScore(self, fname):
        fname = str(fname)
        if not self._isLoadableScore(fname):
            QMessageBox.warning(
                self,
                self.tr("Unsupported file type"),
                self.tr("DrumBurp can only open .brp score files."))
            return
        if self.scoreScene.loadScore(fname):
            self._beatChanged(self.scoreScene.defaultCount)
            self.lilypondSize.setValue(self.scoreScene.score.lilysize)
            self.lilyPagesBox.setValue(self.scoreScene.score.lilypages)
            self.lilyFillButton.setChecked(self.scoreScene.score.lilyFill)
            self._setLilyFormat(self.scoreScene.score.lilyFormat)
            self.filename = str(fname)
            self.updateStatus(self.tr("Successfully loaded %s") % self.filename)
            self._rememberScoreDirectory(self.filename)
            self.addToRecentFiles()
            self.updateRecentFiles()
            self._lilyScene.setNoPreview()

    def _getFileName(self):
        directory = self.filename
        if directory is None:
            suggestion = str(self.scoreScene.title)
            if len(suggestion) == 0:
                suggestion = self.tr("Untitled")
            suggestion = os.extsep.join([suggestion, "brp"])
            directory = self._scoreDialogDirectory()
            directory = os.path.join(directory,
                                     suggestion)
        if os.path.splitext(directory)[-1] == os.extsep + 'brp':
            directory = os.path.splitext(directory)[0]
        caption = self.tr("Choose a DrumBurp file to save")
        fname = QFileDialog.getSaveFileName(parent=self,
                                            caption=caption,
                                            directory=directory,
                                            filter=_scoreFileFilter(self))
        fname = _dialogFilename(fname)
        if len(fname) == 0:
            return False
        if not _isScoreFilename(fname):
            fname = os.extsep.join([str(fname), "brp"])
        self.filename = str(fname)
        self._rememberScoreDirectory(self.filename)
        return True

    def _checkForBackup(self):
        # Returns True if it is OK to continue writing to self.filename,
        # False otherwise
        if self.filename is None:
            return True
        fileFormat = self.scoreScene.score.fileFormat
        if fileFormat is None or fileFormat == CURRENT_FILE_FORMAT:
            return True
        reply = QMessageBox.question(self,
                                     self.tr("Backup old file format?"),
                                     self.tr(
                                         "This score was loaded from an older "
                                         "file format. Would you like to make "
                                         "a backup of that file before overwriting?"),
                                     QMessageBox.Yes,
                                     QMessageBox.No,
                                     QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            backup = self.filename + ".dbff%d.bak" % fileFormat
            if os.path.exists(backup):
                backup += "."
                index = 1
                while os.path.exists(backup + str(index)):
                    index += 1
                backup += str(index)
            try:
                shutil.copyfile(self.filename, backup)
                QMessageBox.warning(self, self.tr("Backup successful"),
                                    self.tr("Old score backed up to %s") % backup)
            except Exception as exc:
                msg = self.tr("Error backing up: %s") % str(exc)
                QMessageBox.warning(self, self.tr("Backup failed"), msg)
                return False
        elif reply == QMessageBox.Cancel:
            return False
        return True

    def fileSave(self):
        if self.filename is None:
            if not self._getFileName():
                return False
        elif not self._checkForBackup():
            return False
        if self.scoreScene.saveScore(self.filename):
            self._rememberScoreDirectory(self.filename)
            self.addToRecentFiles()
            self.updateRecentFiles()
            return True
        return False

    @pyqtSlot()
    def on_actionSave_triggered(self):
        if self.fileSave():
            self.updateStatus(self.tr("Successfully saved %s") % self.filename)

    @pyqtSlot()
    def on_actionSaveAs_triggered(self):
        oldFilename = self.filename
        if self._getFileName():
            if oldFilename == self.filename and not self._checkForBackup():
                return
            self.scoreScene.saveScore(self.filename)
            self.updateStatus("Successfully saved %s" % self.filename)
            self._rememberScoreDirectory(self.filename)
            self.addToRecentFiles()
            self.updateRecentFiles()

    @pyqtSlot()
    def on_actionNew_triggered(self):
        if self.okToContinue():
            counter = self.scoreScene.defaultCount
            registry = self.songProperties.counterRegistry
            dialog = QNewScoreDialog(self,
                                     counter,
                                     registry)
            if dialog.exec():
                nMeasures, counter, kit = dialog.getValues()
                self.scoreScene.newScore(kit,
                                         numMeasures=nMeasures,
                                         counter=counter)
                self.filename = None
                self.updateRecentFiles()
                self._beatChanged(counter)
                self.updateStatus(self.tr("Created a new blank score"))

    def addToRecentFiles(self):
        if (self.filename is not None and
                _isScoreFilename(self.filename) and
                os.path.exists(self.filename)):
            if self.filename in self.recentFiles:
                self.recentFiles.remove(self.filename)
            self.recentFiles.insert(0, self.filename)
            if len(self.recentFiles) > 10:
                self.recentFiles.pop()

    def updateRecentFiles(self):
        self.menuRecentScores.clear()
        self.recentFiles = [fname for fname in self.recentFiles
                            if (_isScoreFilename(fname) and
                                os.path.exists(fname))]
        for fname in self.recentFiles:
            if fname != self.filename and os.path.exists(fname):
                def openRecentFile(bool_, filename=fname):
                    if not self.okToContinue():
                        return
                    self._loadScore(filename)
                action = self.menuRecentScores.addAction(fname)
                action.setIcon(DBIcons.getIcon("score"))
                action.triggered.connect(openRecentFile)

    def _isLoadableScore(self, filename):
        return _isScoreFilename(filename) and os.path.exists(filename)

    def _rememberScoreDirectory(self, filename):
        if filename:
            directory = os.path.dirname(os.path.abspath(str(filename)))
            if os.path.isdir(directory):
                self.lastScoreDirectory = directory

    def _scoreDialogDirectory(self):
        if self.filename:
            directory = os.path.dirname(os.path.abspath(self.filename))
            if os.path.isdir(directory):
                return directory
        if self.lastScoreDirectory and os.path.isdir(self.lastScoreDirectory):
            return self.lastScoreDirectory
        for fname in self.recentFiles:
            directory = os.path.dirname(os.path.abspath(fname))
            if os.path.isdir(directory):
                return directory
        return _homeLocation()

    def _dropScoreFilename(self, event):
        urls = event.mimeData().urls() if event.mimeData().hasUrls() else []
        if len(urls) != 1 or not urls[0].isLocalFile():
            return None
        filename = urls[0].toLocalFile()
        return filename if self._isLoadableScore(filename) else None

    def dragEnterEvent(self, event):
        if self._dropScoreFilename(event) is not None:
            event.acceptProposedAction()
        else:
            event.ignore()

    def dropEvent(self, event):
        filename = self._dropScoreFilename(event)
        if filename is None:
            event.ignore()
            return
        if not self.okToContinue():
            event.ignore()
            return
        self._loadScore(filename)
        event.acceptProposedAction()

    def _beatChanged(self, counter):
        if counter != self.scoreScene.defaultCount:
            self.scoreScene.defaultCount = counter
        self.defaultMeasureButton.setText(counter.countString())

    def _systemSpacingChanged(self, value):
        if value != self.scoreScene.systemSpacing:
            self.scoreScene.systemSpacing = value
        self.lineSpaceSlider.setValue(value)

    def hideEvent(self, event):
        self._state = self.saveState()
        super(DrumBurp, self).hideEvent(event)

    def showEvent(self, event):
        if self._state is not None:
            self.restoreState(self._state)
            self._state = None
        super(DrumBurp, self).showEvent(event)

    @pyqtSlot()
    def on_actionExportASCII_triggered(self):
        fname = self.filename
        if self.filename is None:
            fname = os.path.join(self._scoreDialogDirectory(), 'Untitled.txt')
        if os.path.splitext(fname)[-1] == '.brp':
            fname = os.path.splitext(fname)[0] + '.txt'
        fname = QFileDialog.getSaveFileName(parent=self,
                                            caption=self.tr("Select file to export text tab to"),
                                            directory=fname,
                                            filter=self.tr("Text files (*.txt)"))
        fname = _dialogFilename(fname)
        if not fname:
            return
        try:
            exportedText = self._getTextExport()
        except Exception:
            QMessageBox.warning(self.parent(), self.tr("Text generation failed!"),
                                self.tr("Could not generate text tab for this score!"))
            raise
        try:
            with open(fname, 'w', encoding='utf-8') as txtHandle:
                txtHandle.write(exportedText)
        except Exception:
            QMessageBox.warning(self.parent(), self.tr("Export failed!"),
                                self.tr("Could not export to %s") % fname)
            raise
        else:
            self.updateStatus(self.tr("Successfully exported text tab to %s") % fname)

    def _getTextExport(self):
        props = self.songProperties
        self._asciiSettings = props.generateAsciiSettings(self._asciiSettings)
        self._asciiSettings.underline = self.underlineCheck.isChecked()
        self._asciiSettings.sectionBrackets = self.sectionBracketsCheck.isChecked()
        self._asciiSettings.emptyLineBeforeSection = self.emptyLineBeforeSectionCheck.isChecked()
        self._asciiSettings.emptyLineAfterSection = self.emptyLineAfterSectionCheck.isChecked()
        try:
            asciiBuffer = StringIO()
            exporter = AsciiExport.Exporter(self.scoreScene.score,
                                            self._asciiSettings)
            exporter.export(asciiBuffer)
        except Exception:
            self.textExportPreview.setPlainText(self.tr("Failed to export text tab."))
            raise
        return asciiBuffer.getvalue()

    def _refreshTextExport(self):
        try:
            self.textExportPreview.setPlainText(self._getTextExport())
            self.actionExportASCII.setEnabled(True)
            self.textExportButton.setEnabled(True)
        except Exception:
            self.textExportPreview.setPlainText("Failed to export text tab.")
            self.actionExportASCII.setEnabled(False)
            self.textExportButton.setEnabled(False)
            raise

    @pyqtSlot()
    def on_actionPrint_triggered(self):
        if self._printer is None:
            self._printer = QPrinter()
        self._printer = QPrinter(QPrinterInfo(self._printer),
                                 QPrinter.HighResolution)
        self._printer.setPaperSize(self._getPaperSize())
        dialog = QPrintPreviewDialog(self._printer, parent=self)

        def updatePages(qprinter):
            self.scoreScene.printScore(qprinter, self.scoreView)
        dialog.paintRequested.connect(updatePages)
        dialog.exec()

    @pyqtSlot()
    def on_actionExportPDF_triggered(self):
        try:
            printer = QPrinter(mode=QPrinter.HighResolution)
            printer.setPaperSize(self._getPaperSize())
            printer.setOutputFormat(QPrinter.PdfFormat)
            if self.filename:
                outfileName = list(os.path.splitext(self.filename)[:-1])
                outfileName = os.extsep.join(outfileName + ["pdf"])
            else:
                outfileName = "Untitled.pdf"
            printer.setOutputFileName(outfileName)
            printer.setPaperSize(self._getPaperSize())
            dialog = QPrintPreviewDialog(printer, parent=self)

            def updatePages(qprinter):
                self.scoreScene.printScore(qprinter, self.scoreView)
            dialog.paintRequested.connect(updatePages)
            dialog.exec()
            self.updateStatus(self.tr("Exported to PDF %s") % outfileName)
        except Exception:
            QMessageBox.warning(self.parent(), "Export failed!",
                                self.tr("Could not export PDF to %s") % outfileName)

    @pyqtSlot()
    def on_actionExportLilypond_triggered(self):
        self.checkLilypondPath()
        lilyBuffer = StringIO()
        try:
            lyScore = LilypondScore(self.scoreScene.score)
            lyScore.write(lilyBuffer)
        except LilypondProblem as exc:
            QMessageBox.warning(self.parent(), self.tr("Lilypond impossible"),
                                self.tr("Cannot export Lilypond for this score: %s")
                                % exc.__doc__)
        except Exception as exc:
            QMessageBox.warning(self.parent(), "Export failed!",
                                self.tr("Error generating Lilypond for this score: %s")
                                % exc.__doc__)
            raise
        else:
            try:
                if self.filename:
                    filestem = os.path.splitext(self.filename)[:-1]
                    outfileName = os.path.extsep.join(filestem)
                    directory = os.path.abspath(outfileName)
                else:
                    outfileName = "Untitled.ly"
                    directory = os.path.join(self._scoreDialogDirectory(),
                                             outfileName)
                caption = self.tr("Choose a Lilypond input file to write to")
                fname = QFileDialog.getSaveFileName(parent=self,
                                                    caption=caption,
                                                    directory=directory,
                                                    filter="(*.ly)")
                fname = _dialogFilename(fname)
                if len(fname) == 0:
                    return
                fname = str(fname)
                if self._exporter is not None:
                    if self._exporter.isRunning():
                        QMessageBox.warning(self.parent(), self.tr("Still exporting"),
                                            self.tr("Cannot export now - previous export is still in progress"))
                        return
                self._exporter = LilypondExporter(lilyBuffer.getvalue(), fname,
                                                  self.lilyPath,
                                                  self.scoreScene.score.lilyFormat,
                                                  lambda: self.exporterDone.emit(
                                                      fname),
                                                  self)
                self.setLilypondControlsEnabled(False)
                self._exporter.start()
            except Exception:
                QMessageBox.warning(self.parent(), "Export failed!",
                                    self.tr("Could not export Lilypond"))
                raise

    def setLilypondControlsEnabled(self, onOff):
        self.actionExportLilypond.setEnabled(onOff)
        self.lilypondGroupBox.setEnabled(onOff)

    def _finishLilyExport(self, fname):
        self.setLilypondControlsEnabled(True)
        status = self._exporter.get_status()
        if status == self._exporter.SUCCESS:
            self.updateStatus(self.tr("Successfully ran Lilypond on %s") % fname)
        elif status == self._exporter.WROTE_LY:
            self.updateStatus(self.tr("Successfully exported Lilypond to %s") % fname)
        elif status == self._exporter.ERROR_IN_WRITING_LY:
            QMessageBox.warning(self.parent(), "Export failed!",
                                self.tr("Could not write Lilypond score to %s") % fname)
        elif status == self._exporter.ERROR_IN_RUNNING_LY:
            QMessageBox.warning(self.parent(), "Export failed!",
                                self.tr("Could not run Lilypond on %s") % fname)

    # ── Language menu ────────────────────────────────────────────────────────

    # Human-readable names for each language code.
    _LANGUAGE_NAMES = {
        "en": "English",
        "es": "Español",
        "fr": "Français",
        "de": "Deutsch",
        "pt": "Português",
        "it": "Italiano",
        "ja": "日本語",
    }

    def _buildLanguageMenu(self):
        """Build the Language submenu under Help from available .qm files."""
        import glob
        from i18n.i18n import _i18n_dir

        qm_files = sorted(glob.glob(os.path.join(_i18n_dir(), "drumburp_*.qm")))
        if not qm_files:
            return

        # Read current saved language
        settings = self._makeQSettings()
        current_lang = _settingsValue(settings, "Language", "", str) or ""

        lang_menu = self.menuHelp.addMenu(self.tr("Language"))
        lang_group = QActionGroup(self)
        lang_group.setExclusive(True)

        import re
        for qm in qm_files:
            code = re.search(r"drumburp_(.+)\.qm", qm).group(1)
            name = self._LANGUAGE_NAMES.get(code, code.upper())
            action = QAction(name, self)
            action.setCheckable(True)
            action.setChecked(code == current_lang or
                              (not current_lang and code == "en"))
            action.setData(code)
            action.triggered.connect(
                lambda checked, c=code: self._selectLanguage(c))
            lang_group.addAction(action)
            lang_menu.addAction(action)

    def _selectLanguage(self, lang_code):
        """Save the chosen language and prompt the user to restart."""
        settings = self._makeQSettings()
        settings.setValue("Language", lang_code)
        settings.sync()
        QMessageBox.information(
            self,
            self.tr("Language changed"),
            self.tr("The language will change the next time DrumBurp starts."))

    @pyqtSlot()
    def on_actionWhatsThis_triggered(self):
        QWhatsThis.enterWhatsThisMode()

    @pyqtSlot()
    def on_actionUndo_triggered(self):
        self.scoreScene.undo()

    @pyqtSlot()
    def on_actionRedo_triggered(self):
        self.scoreScene.redo()

    @pyqtSlot()
    def on_actionAboutDrumBurp_triggered(self):
        dlg = DBInfoDialog(DB_VERSION, self)
        dlg.exec()

    @pyqtSlot()
    def on_actionOnlineManual_triggered(self):
        webbrowser.open_new_tab("https://github.com/wachin/DrumBurp/wiki")

    def _getPaperSize(self):
        try:
            return getattr(QPrinter, str(self.paperBox.currentText()))
        except AttributeError:
            return QPrinter.Letter

    @pyqtSlot()
    def on_actionFitPage_triggered(self):
        papersize = self._getPaperSize()
        printer = QPrinter()
        printer.setPaperSize(papersize)
        widthInPixels = printer.pageRect().width()
        maxColumns = self.songProperties.maxColumns(widthInPixels)
        self.widthSpinBox.setValue(maxColumns)
        self.scoreScene.reBuild()

    @pyqtSlot()
    def on_defaultMeasureButton_clicked(self):
        counter = self.scoreScene.defaultCount
        dlg = QEditMeasureDialog(counter, counter,
                                 self.songProperties.counterRegistry,
                                 self)
        if dlg.exec():
            counter = dlg.getValues()
            self._beatChanged(counter)

    def setPaperSize(self, paperSize):
        index = self.paperBox.findText(paperSize)
        if index > -1 and index != self.paperBox.currentIndex():
            self.paperBox.setCurrentIndex(index)
        elif index == -1:
            self.paperBox.setCurrentIndex(0)

    def setDefaultCount(self, count):
        self._beatChanged(count)

    def setSystemSpacing(self, value):
        self._systemSpacingChanged(value)

    def setSections(self):
        score = self.scoreScene.score
        self.sectionNavigator.blockSignals(True)
        self.sectionNavigator.clear()
        for sectionTitle in score.iterSections():
            self.sectionNavigator.addItem(_displaySectionTitle(sectionTitle),
                                          sectionTitle)
        self.sectionNavigator.blockSignals(False)

    def _refreshMidiDevices(self):
        self.menuSelectMidiOut.clear()
        self.menuSelectMidiOut.addAction(self.actionRefreshMidiDevices)
        self.menuSelectMidiOut.addSeparator()
        DBMidi.refreshOutputDevices()
        current = DBMidi.currentDevice()
        hasDevices = False
        for device in DBMidi.iterMidiDevices():
            hasDevices = True
            action = QAction(device.name, self.menuSelectMidiOut,
                             checkable=True)
            self.menuSelectMidiOut.addAction(action)

            def selectDevice(unused, dev=device):
                selected = DBMidi.selectMidiDevice(dev)
                self._refreshMidiDevices()
                self._setMidiPlaybackEnabled(DBMidi.HAS_MIDI)
                if selected:
                    self.statusbar.showMessage(
                        self.tr("MIDI output: %s") % dev.name, 5000)
                else:
                    QMessageBox.warning(
                        self, self.tr("MIDI output unavailable"),
                        self.tr("Could not open MIDI output device:\n%s")
                        % dev.name)
            action.triggered.connect(selectDevice)
            action.setChecked(device == current)
        if not hasDevices:
            action = QAction(self.tr("No MIDI output devices found"),
                             self.menuSelectMidiOut)
            action.setEnabled(False)
            self.menuSelectMidiOut.addAction(action)
        self.menuSelectMidiOut.setEnabled(True)

    @pyqtSlot()
    def on_actionRefreshMidiDevices_triggered(self):
        self._refreshMidiDevices()

    def _canPlayback(self):
        try:
            unused = list(self.scoreScene.score.iterMeasuresWithRepeats())
        except InconsistentRepeats as exc:
            QMessageBox.warning(self, self.tr("Playback error"),
                                self.tr("There are inconsistent repeat markings."))
            position = self.scoreScene.score.measureIndexToPosition(exc[0])
            measure = self.scoreScene.getQMeasure(position)
            self.scoreView.showItemAtTop(measure)
            return False
        return True

    @pyqtSlot(bool)
    def on_actionPlayScore_toggled(self, onOff):
        if onOff:
            self.tabWidget.setCurrentWidget(self.textTab)
            self.scoreView.setTopLeft(0, 0)
            if not self._canPlayback():
                self.actionPlayScore.toggle()
                return
            DBMidi.playScore(self.scoreScene.score)
            self.musicStart()
        else:
            self.musicDone()
            DBMidi.shutUp()

    def highlightPlayingMeasure(self, index, nextIndex):
        measure = None
        nextMeasure = None
        if index == -1:
            self.scoreScene.highlightPlayingMeasure(None)
        else:
            position = self.scoreScene.score.measureIndexToPosition(index)
            self.scoreScene.highlightPlayingMeasure(position)
            measure = self.scoreScene.getQMeasure(position)
        if nextIndex == -1:
            self.scoreScene.highlightNextMeasure(None)
        else:
            position = self.scoreScene.score.measureIndexToPosition(nextIndex)
            self.scoreScene.highlightNextMeasure(position)
            nextMeasure = self.scoreScene.getQMeasure(position)
        if measure:
            if nextMeasure:
                self.scoreView.showTwoItems(measure, nextMeasure)
            else:
                self.scoreView.showItemAtTop(measure)

    @pyqtSlot(bool)
    def on_actionMuteNotes_toggled(self, onOff):
        DBMidi.setMute(onOff)

    @pyqtSlot()
    def on_actionExportMIDI_triggered(self):
        if not self._canPlayback():
            return
        try:
            midiBuffer = BytesIO()
            DBMidi.exportMidi(self.scoreScene.score.iterMeasuresWithRepeats(),
                              self.scoreScene.score, midiBuffer)
        except Exception as exc:
            QMessageBox.warning(self.parent(), self.tr("Error generating MIDI!"),
                                self.tr("Failed to generate MIDI for this score: %s")
                                % exc.__doc__)
            raise
        directory = self.filename
        if directory is None:
            suggestion = str(self.scoreScene.title)
            if len(suggestion) == 0:
                suggestion = self.tr("Untitled")
            suggestion = os.extsep.join([suggestion, "brp"])
            directory = self._scoreDialogDirectory()
            directory = os.path.join(directory,
                                     suggestion)
        if os.path.splitext(directory)[-1] == os.extsep + 'brp':
            directory = os.path.splitext(directory)[0]
        caption = self.tr("Export to MIDI")
        fname = QFileDialog.getSaveFileName(parent=self,
                                            caption=caption,
                                            directory=directory,
                                            filter=self.tr("DrumBurp files (*.mid)"))
        fname = _dialogFilename(fname)
        if len(fname) == 0:
            return
        try:
            with open(fname, 'wb') as handle:
                handle.write(midiBuffer.getvalue())
        except Exception:
            QMessageBox.warning(self.parent(), self.tr("File error"),
                                self.tr("Error writing MIDI to file %s") % fname)

    @pyqtSlot(bool)
    def on_actionLoopBars_toggled(self, onOff):
        if onOff:
            self.tabWidget.setCurrentWidget(self.textTab)
            if not self.scoreScene.hasDragSelection():
                self.actionLoopBars.toggle()
                return
            DBMidi.loopBars(self.scoreScene.iterDragSelection(),
                            self.scoreScene.score)
            self.musicStart()
        else:
            self.musicDone()
            DBMidi.shutUp()

    @pyqtSlot(bool)
    def on_actionPlayOnce_toggled(self, onOff):
        if onOff:
            self.tabWidget.setCurrentWidget(self.textTab)
            if not self.scoreScene.hasDragSelection():
                self.actionPlayOnce.toggle()
                return
            DBMidi.loopBars(self.scoreScene.iterDragSelection(),
                            self.scoreScene.score,
                            loopCount=1)
            self.musicStart()
        else:
            self.musicDone()
            DBMidi.shutUp()

    @pyqtSlot()
    def on_actionCopyMeasures_triggered(self):
        self.scoreScene.copyMeasures()

    def checkPasteMeasure(self):
        onOff = (self.scoreScene.hasDragSelection() and
                 len(self.scoreScene.measureClipboard) > 0)
        self.actionPasteMeasures.setEnabled(onOff)
        self.actionFillPasteMeasures.setEnabled(onOff)

    @pyqtSlot()
    def on_actionPasteMeasures_triggered(self):
        self.scoreScene.pasteMeasuresOver()

    @pyqtSlot()
    def on_actionFillPasteMeasures_triggered(self):
        self.scoreScene.pasteMeasuresOver(repeating=True)

    @pyqtSlot()
    def on_actionClearMeasures_triggered(self):
        self.scoreScene.clearMeasures()

    @pyqtSlot()
    def on_actionDeleteMeasures_triggered(self):
        self.scoreScene.deleteMeasures()

    def musicStart(self):
        self.tabWidget.setCurrentWidget(self.textTab)
        self.scoreScene.sendFsmEvent(StartPlaying())

    def musicDone(self):
        players = [self.actionPlayScore, self.actionPlayOnce,
                   self.actionLoopBars]
        for playButton in players:
            if playButton.isChecked():
                playButton.setChecked(False)
        self.scoreScene.sendFsmEvent(StopPlaying())

    def _scorePlaying(self, playing):
        self.fileToolBar.setDisabled(playing)
        self.displayToolBar.setDisabled(playing)
        self.helpToolBar.setDisabled(playing)
        self.fontDock.setDisabled(playing)
        self.scorePropertiesGroup.setDisabled(playing)
        self.menubar.setDisabled(playing)
        self.actionExportMIDI.setDisabled(playing)
        self.actionMuteNotes.setDisabled(playing)
        self.lilypondGroupBox.setDisabled(playing)
        self.scoreView.horizontalScrollBar().setDisabled(playing)
        self.scoreView.verticalScrollBar().setDisabled(playing)
        self.scoreActionsBox.setDisabled(playing)
        self.refreshLilypond.setDisabled(playing)
        self.textExportOptions.setDisabled(playing)

    @pyqtSlot(int)
    def on_paperBox_currentIndexChanged(self, index):
        if not isinstance(index, int):
            index = self.paperBox.findText(str(index))
        if index < 0 or index >= len(self._knownPageHeights):
            return
        self._pageHeight = self._knownPageHeights[index]
        self.sceneFormatted()

    def sceneFormatted(self):
        if self.scoreScene:
            numMeasures = self.scoreScene.score.numMeasures()
            measureText = self.tr("%n Measure(s)", "", numMeasures)
            numStaffs = self.scoreScene.score.numStaffs()
            staffText = self.tr("%n Staff(s)", "", numStaffs)
            numPages = self.scoreScene.numPages(self._pageHeight)
            pageText = self.tr("%n Page(s)", "", numPages)
            self._infoBar.setText(", ".join([measureText, staffText, pageText]))

    def _setStatusFromScene(self, msg):
        self.statusbar.showMessage(msg)

    def _setLilySize(self, size):
        if size != self.lilypondSize.value():
            self.lilypondSize.setValue(size)

    def _setLilyPages(self, numPages):
        if numPages != self.lilyPagesBox.value():
            self.lilyPagesBox.setValue(numPages)

    def _setLilyFill(self, lilyFill):
        if lilyFill != self.lilyFillButton.isChecked():
            self.lilyFillButton.setChecked(lilyFill)

    def _setLilyFormat(self, lilyFormat):
        if lilyFormat < 0 or lilyFormat > 2:
            lilyFormat = 0
        target = [self.lilyPdfButton, self.lilyPsButton,
                  self.lilyPngButton][lilyFormat]
        if not target.isChecked():
            target.setChecked(True)
        self.scoreScene.setLilyFormat(lilyFormat)

    @pyqtSlot()
    def on_actionCheckForUpdates_triggered(self):
        dialog = QVersionDownloader(newer=None, parent=self)
        dialog.exec()

    def _finishedVersionCheck(self):
        newer = self._versionThread.newVersionInfo
        if newer:
            dialog = QVersionDownloader(newer=newer, parent=self)
            dialog.exec()
        elif newer is None:
            self.statusbar.showMessage(
                self.tr("Failed to get latest version info from www.whatang.org"), 5000)
        else:
            self.statusbar.showMessage(
                self.tr("Check successful: You have the latest version of DrumBurp"), 5000)

    def _midiInitFinished(self):
        self._refreshMidiDevices()
        self.menu_MIDI.setEnabled(True)
        self.MIDIToolBar.setEnabled(True)
        self._setMidiPlaybackEnabled(DBMidi.HAS_MIDI)
        self.setEnabled(True)

    @pyqtSlot()
    def on_actionEditColours_triggered(self):
        dialog = DBColourPicker.DBColourPicker(self.colourScheme, self)
        if not dialog.exec():
            return
        self.colourScheme = dialog.getColourScheme()
        self.scoreView.update()
        self.scoreScene.recolor()

    def checkLilypondPath(self, existing=None):
        if not existing and not self.lilyPath:
            QMessageBox.information(self, "Lilypond",
                                    self.tr(
                                        "Lilypond is a program for displaying music "
                                        "notation. DrumBurp can export Lilypond files "
                                        "and use Lilypond to display your drum score "
                                        "as sheet music. First you must download "
                                        "and install Lilypond from www.lilypond.org "
                                        "and set the path to the lilypond program in "
                                        "this window."),
                                    buttons=QMessageBox.Ok,
                                    defaultButton=QMessageBox.Ok)
        if (self.lilyPath is None
            or not os.path.exists(self.lilyPath)
                or existing is not None):
            caption = self.tr("Please select path to Lilypond executable")
            path = QFileDialog.getOpenFileName(parent=self,
                                               caption=caption,
                                               directory=existing)
            path = _dialogFilename(path)
            if not path and existing:
                path = existing
            if not path or not os.path.exists(path):
                self.lilyPreviewControls.setEnabled(False)
                return
            self.lilyPreviewControls.setEnabled(True)
            self.lilyPath = _normalisePath(path)

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, tabIndex_):
        widget = self.tabWidget.currentWidget()
        if widget == self.textTab:
            self.availableNotesLabel.setVisible(True)
            self._infoBar.setVisible(True)
        elif widget == self.lilypondTab:
            self.availableNotesLabel.setVisible(False)
            self._infoBar.setVisible(False)
            self.checkLilypondPath()
        elif widget == self.textExportTab:
            self.availableNotesLabel.setVisible(False)
            self._infoBar.setVisible(False)

    @pyqtSlot()
    def on_lilypondPathButton_clicked(self):
        self.checkLilypondPath(self.lilyPath)

    @pyqtSlot()
    def on_lilyPdfButton_clicked(self):
        self._setLilyFormat(0)

    @pyqtSlot()
    def on_lilyPsButton_clicked(self):
        self._setLilyFormat(1)

    @pyqtSlot()
    def on_lilyPngButton_clicked(self):
        self._setLilyFormat(2)


class VersionCheckThread(QThread):
    def __init__(self, parent=None):
        super(VersionCheckThread, self).__init__(parent=parent)
        self.newVersionInfo = None

    def run(self):
        self.newVersionInfo = doesNewerVersionExist()
