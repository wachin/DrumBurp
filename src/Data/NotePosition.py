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
Created on 14 Dec 2010

@author: Mike Thomas
'''

from Data.DBErrors import BadNoteSpecification
import copy


class NotePosition(object):
    def __init__(self, staffIndex=None, measureIndex=None,
                 noteTime=None, drumIndex=None):
        if [noteTime, drumIndex].count(None) == 1:
            raise BadNoteSpecification(staffIndex, measureIndex,
                                       noteTime, drumIndex)
        self.staffIndex = staffIndex
        self.measureIndex = measureIndex
        self.noteTime = noteTime
        self.drumIndex = drumIndex

    def __str__(self):
        return ", ".join(str(x) for x in [self.staffIndex, self.measureIndex,
                                          self.noteTime, self.drumIndex])

    def __repr__(self):
        return "NotePosition(%s, %s, %s, %s)" % (str(self.staffIndex),
                                                 str(self.measureIndex),
                                                 str(self.noteTime),
                                                 str(self.drumIndex))

    def makeCopy(self):
        return copy.copy(self)

    def makeMeasurePosition(self):
        np = self.makeCopy()
        np.noteTime = None
        np.drumIndex = None
        return np

    def makeStaffPosition(self):
        np = self.makeMeasurePosition()
        np.measureIndex = None
        return np

    def _key(self):
        # None values sort before any integer (use -1 as sentinel for None)
        def _v(x):
            return (0, -1) if x is None else (1, x)
        return (_v(self.staffIndex), _v(self.measureIndex),
                _v(self.noteTime), _v(self.drumIndex))

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, NotePosition):
            return NotImplemented
        return (self.staffIndex == other.staffIndex and
                self.measureIndex == other.measureIndex and
                self.noteTime == other.noteTime and
                self.drumIndex == other.drumIndex)

    def __lt__(self, other):
        if other is None:
            return False  # self > None, so self is not less than None
        if not isinstance(other, NotePosition):
            return NotImplemented
        return self._key() < other._key()

    def __le__(self, other):
        return self == other or self < other

    def __gt__(self, other):
        if other is None:
            return True  # self > None always
        if not isinstance(other, NotePosition):
            return NotImplemented
        return self._key() > other._key()

    def __ge__(self, other):
        return self == other or self > other

    def __hash__(self):
        return hash((self.staffIndex, self.measureIndex,
                     self.noteTime, self.drumIndex))
