# Copyright 2026 Washington Indacochea Delgado
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from PyQt5 import QtCore


def translatedCountName(name):
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
