# -*- coding: utf-8 -*-
"""Compatibility stub for legacy pyrcc4 resources.

The PyQt5 UI loads these images directly through GUI.QtResourceCompat.
Do not register the old pyrcc4 payload here; it can crash under PyQt5.
"""


def qInitResources():
    pass


def qCleanupResources():
    pass
