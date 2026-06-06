# Copyright 2026 Washington Indacochea Delgado
#
# This file is part of DrumBurp.
#
# DrumBurp is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

from PyQt5.QtCore import QCoreApplication


def _bilingual(name, translated):
    if translated == name:
        return name
    return "%s (%s)" % (name, translated)


def displayDrumName(name):
    names = {
        "Crash": QCoreApplication.translate("DBDrumDisplay", "Crash"),
        "Crash Cymbal": QCoreApplication.translate(
            "DBDrumDisplay", "Crash Cymbal"),
        "Crash Cymbal 1": QCoreApplication.translate(
            "DBDrumDisplay", "Crash Cymbal 1"),
        "Crash Cymbal 2": QCoreApplication.translate(
            "DBDrumDisplay", "Crash Cymbal 2"),
        "Crash-ride cymbal": QCoreApplication.translate(
            "DBDrumDisplay", "Crash-ride cymbal"),
        "Crash cymbal": QCoreApplication.translate(
            "DBDrumDisplay", "Crash cymbal"),
        "Ride": QCoreApplication.translate("DBDrumDisplay", "Ride"),
        "Ride Cymbal": QCoreApplication.translate(
            "DBDrumDisplay", "Ride Cymbal"),
        "HiHat": QCoreApplication.translate("DBDrumDisplay", "HiHat"),
        "Hihat": QCoreApplication.translate("DBDrumDisplay", "Hihat"),
        "Hi hat w/foot": QCoreApplication.translate(
            "DBDrumDisplay", "Hi hat w/foot"),
        "Hihat w/foot": QCoreApplication.translate(
            "DBDrumDisplay", "Hihat w/foot"),
        "Hi-Hat with foot": QCoreApplication.translate(
            "DBDrumDisplay", "Hi-Hat with foot"),
        "High hat foot": QCoreApplication.translate(
            "DBDrumDisplay", "High hat foot"),
        "Foot pedal": QCoreApplication.translate(
            "DBDrumDisplay", "Foot pedal"),
        "Kick": QCoreApplication.translate("DBDrumDisplay", "Kick"),
        "Bass Drum": QCoreApplication.translate(
            "DBDrumDisplay", "Bass Drum"),
        "Bass Drum 1": QCoreApplication.translate(
            "DBDrumDisplay", "Bass Drum 1"),
        "Bass Drum 2": QCoreApplication.translate(
            "DBDrumDisplay", "Bass Drum 2"),
        "Bass drum": QCoreApplication.translate(
            "DBDrumDisplay", "Bass drum"),
        "Snare": QCoreApplication.translate("DBDrumDisplay", "Snare"),
        "Snare Drum": QCoreApplication.translate(
            "DBDrumDisplay", "Snare Drum"),
        "Second snare": QCoreApplication.translate(
            "DBDrumDisplay", "Second snare"),
        "High Tom": QCoreApplication.translate(
            "DBDrumDisplay", "High Tom"),
        "Mid Tom": QCoreApplication.translate(
            "DBDrumDisplay", "Mid Tom"),
        "Small Tom": QCoreApplication.translate(
            "DBDrumDisplay", "Small Tom"),
        "Tom 1": QCoreApplication.translate("DBDrumDisplay", "Tom 1"),
        "Tom 2": QCoreApplication.translate("DBDrumDisplay", "Tom 2"),
        "Tom 3": QCoreApplication.translate("DBDrumDisplay", "Tom 3"),
        "Tom 4": QCoreApplication.translate("DBDrumDisplay", "Tom 4"),
        "Floor Tom": QCoreApplication.translate(
            "DBDrumDisplay", "Floor Tom"),
        "Floor Tom 1": QCoreApplication.translate(
            "DBDrumDisplay", "Floor Tom 1"),
        "Floor Tom 2": QCoreApplication.translate(
            "DBDrumDisplay", "Floor Tom 2"),
        "Percussion Line 1": QCoreApplication.translate(
            "DBDrumDisplay", "Percussion Line 1"),
        "Percussion Line 2": QCoreApplication.translate(
            "DBDrumDisplay", "Percussion Line 2"),
        "Cymbal": QCoreApplication.translate("DBDrumDisplay", "Cymbal"),
    }
    return _bilingual(name, names.get(name, name))


def displayMidiNoteName(name):
    names = {
        "Acoustic Bass Drum": QCoreApplication.translate(
            "DBDrumDisplay", "Acoustic Bass Drum"),
        "Bass Drum 1": QCoreApplication.translate(
            "DBDrumDisplay", "Bass Drum 1"),
        "Side Stick": QCoreApplication.translate(
            "DBDrumDisplay", "Side Stick"),
        "Acoustic Snare": QCoreApplication.translate(
            "DBDrumDisplay", "Acoustic Snare"),
        "Hand Clap": QCoreApplication.translate(
            "DBDrumDisplay", "Hand Clap"),
        "Electric Snare": QCoreApplication.translate(
            "DBDrumDisplay", "Electric Snare"),
        "Low Floor Tom": QCoreApplication.translate(
            "DBDrumDisplay", "Low Floor Tom"),
        "Closed Hi Hat": QCoreApplication.translate(
            "DBDrumDisplay", "Closed Hi Hat"),
        "High Floor Tom": QCoreApplication.translate(
            "DBDrumDisplay", "High Floor Tom"),
        "Pedal Hi Hat": QCoreApplication.translate(
            "DBDrumDisplay", "Pedal Hi Hat"),
        "Low Tom": QCoreApplication.translate(
            "DBDrumDisplay", "Low Tom"),
        "Open Hi Hat": QCoreApplication.translate(
            "DBDrumDisplay", "Open Hi Hat"),
        "Low-Mid Tom": QCoreApplication.translate(
            "DBDrumDisplay", "Low-Mid Tom"),
        "Hi-Mid Tom": QCoreApplication.translate(
            "DBDrumDisplay", "Hi-Mid Tom"),
        "Crash Cymbal 1": QCoreApplication.translate(
            "DBDrumDisplay", "Crash Cymbal 1"),
        "High Tom": QCoreApplication.translate(
            "DBDrumDisplay", "High Tom"),
        "Ride Cymbal 1": QCoreApplication.translate(
            "DBDrumDisplay", "Ride Cymbal 1"),
        "Chinese Cymbal": QCoreApplication.translate(
            "DBDrumDisplay", "Chinese Cymbal"),
        "Ride Bell": QCoreApplication.translate(
            "DBDrumDisplay", "Ride Bell"),
        "Tambourine": QCoreApplication.translate(
            "DBDrumDisplay", "Tambourine"),
        "Splash Cymbal": QCoreApplication.translate(
            "DBDrumDisplay", "Splash Cymbal"),
        "Cowbell": QCoreApplication.translate(
            "DBDrumDisplay", "Cowbell"),
        "Crash Cymbal 2": QCoreApplication.translate(
            "DBDrumDisplay", "Crash Cymbal 2"),
        "Vibraslap": QCoreApplication.translate(
            "DBDrumDisplay", "Vibraslap"),
        "Ride Cymbal 2": QCoreApplication.translate(
            "DBDrumDisplay", "Ride Cymbal 2"),
        "Hi Bongo": QCoreApplication.translate(
            "DBDrumDisplay", "Hi Bongo"),
        "Low Bongo": QCoreApplication.translate(
            "DBDrumDisplay", "Low Bongo"),
        "Mute Hi Conga": QCoreApplication.translate(
            "DBDrumDisplay", "Mute Hi Conga"),
        "Open Hi Conga": QCoreApplication.translate(
            "DBDrumDisplay", "Open Hi Conga"),
        "Low Conga": QCoreApplication.translate(
            "DBDrumDisplay", "Low Conga"),
        "High Timbale": QCoreApplication.translate(
            "DBDrumDisplay", "High Timbale"),
        "Low Timbale": QCoreApplication.translate(
            "DBDrumDisplay", "Low Timbale"),
        "High Agogo": QCoreApplication.translate(
            "DBDrumDisplay", "High Agogo"),
        "Low Agogo": QCoreApplication.translate(
            "DBDrumDisplay", "Low Agogo"),
        "Cabasa": QCoreApplication.translate(
            "DBDrumDisplay", "Cabasa"),
        "Maracas": QCoreApplication.translate(
            "DBDrumDisplay", "Maracas"),
        "Short Whistle": QCoreApplication.translate(
            "DBDrumDisplay", "Short Whistle"),
        "Long Whistle": QCoreApplication.translate(
            "DBDrumDisplay", "Long Whistle"),
        "Short Guiro": QCoreApplication.translate(
            "DBDrumDisplay", "Short Guiro"),
        "Long Guiro": QCoreApplication.translate(
            "DBDrumDisplay", "Long Guiro"),
        "Claves": QCoreApplication.translate(
            "DBDrumDisplay", "Claves"),
        "Hi Wood Block": QCoreApplication.translate(
            "DBDrumDisplay", "Hi Wood Block"),
        "Low Wood Block": QCoreApplication.translate(
            "DBDrumDisplay", "Low Wood Block"),
        "Mute Cuica": QCoreApplication.translate(
            "DBDrumDisplay", "Mute Cuica"),
        "Open Cuica": QCoreApplication.translate(
            "DBDrumDisplay", "Open Cuica"),
        "Mute Triangle": QCoreApplication.translate(
            "DBDrumDisplay", "Mute Triangle"),
        "Open Triangle": QCoreApplication.translate(
            "DBDrumDisplay", "Open Triangle"),
    }
    return _bilingual(name, names.get(name, name))
