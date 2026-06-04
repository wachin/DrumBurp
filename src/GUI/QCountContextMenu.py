# Copyright 2014 Michael Thomas
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
Created on May 11, 2014

@author: Mike Thomas
'''
# import copy

from GUI.QMenuIgnoreCancelClick import QMenuIgnoreCancelClick
from GUI.DBCommands import (ChangeMeasureCountCommand,
                            ContractMeasureCountCommand,
                            ContractAllMeasureCountsCommand)
from Data.MeasureCount import makeSimpleCount
from GUI.DBFSMEvents import EditMeasureProperties
from PyQt5 import QtCore


class QCountContextMenu(QMenuIgnoreCancelClick):
    def __init__(self, qScore, np, qmeasure):
        super(QCountContextMenu, self).__init__(qScore)
        self._np = np
        self._qmeasure = qmeasure
        self._measure = self._qScore.score.getMeasureByPosition(self._np)
        self._counter = self._measure.counter
        self._setup()

    def _setup(self):
        if not self._measure.simileDistance > 0:
            self.addAction(self.tr("Edit Measure Count"),
                           self._editMeasureCount)
            measureMenu = self.addMenu(self.tr("Measure Count"))
            self._addCountActions(measureMenu, self._setMeasureCount)
            self.addSeparator()
            self.addSeparator()
            contractAction = self.addAction(self.tr("Contract Count"),
                                            self._contractCount)
            contractAction.setEnabled(
                self._measure.getSmallestSimpleCount() != None)
        self.addAction(self.tr("Contract All Counts"),
                       self._contractAllCounts)

    def _addCountActions(self, menu, countFunction):
        for name, counter in self._qScore.displayProperties.counterRegistry:
            menu.addAction(self._translatedCountName(name),
                           lambda beat=counter: countFunction(beat))

    def _translatedCountName(self, name):
        names = {
            "Quarter Notes": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "Quarter Notes"),
            "8ths": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "8ths"),
            "Triplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "Triplets"),
            "Quintuplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "Quintuplets"),
            "Septuplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "Septuplets"),
            "16ths": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "16ths"),
            "Sparse 16ths": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "Sparse 16ths"),
            "16th Triplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "16th Triplets"),
            "Sparse 16th Triplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "Sparse 16th Triplets"),
            "16th Quintuplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "16th Quintuplets"),
            "16th Septuplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "16th Septuplets"),
            "32nds": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "32nds"),
            "Sparse 32nds": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "Sparse 32nds"),
            "32nd Triplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "32nd Triplets"),
            "Sparse 32nd Triplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "Sparse 32nd Triplets"),
            "32nd Quintuplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "32nd Quintuplets"),
            "32nd Septuplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "32nd Septuplets"),
            "64ths": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "64ths"),
            "Sparse 64ths": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "Sparse 64ths"),
            "64th Triplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "64th Triplets"),
            "Sparse 64th Triplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "Sparse 64th Triplets"),
            "64th Quintuplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "64th Quintuplets"),
            "64th Septuplets": QtCore.QCoreApplication.translate(
                "QCountContextMenu", "64th Septuplets"),
        }
        translatedName = names.get(name, name)
        if translatedName == name:
            return name
        return "%s (%s)" % (name, translatedName)

    @QMenuIgnoreCancelClick.menuSelection
    def _setMeasureCount(self, newCounter):
        newMeasureCount = makeSimpleCount(newCounter,
                                          self._counter.numBeats())
        command = ChangeMeasureCountCommand(self._qScore, self._np,
                                            newMeasureCount)
        self._qScore.addCommand(command)

    @QMenuIgnoreCancelClick.menuSelection
    def _contractCount(self):
        command = ContractMeasureCountCommand(self._qScore, self._np)
        self._qScore.clearDragSelection()
        self._qScore.addCommand(command)

    @QMenuIgnoreCancelClick.menuSelection
    def _contractAllCounts(self):
        command = ContractAllMeasureCountsCommand(self._qScore, self._np)
        self._qScore.clearDragSelection()
        self._qScore.addCommand(command)

    def _editMeasureCount(self):
        fsmEvent = EditMeasureProperties(self._counter,
                                         self._props.counterRegistry,
                                         self._np)
        self._qScore.sendFsmEvent(fsmEvent)
