# -*- coding: utf-8 -*-
"""Compatibility stub for legacy pyrcc4 resources.

The generated PyQt5 UI files use GUI.QtResourceCompat to resolve resource
paths to real files. Keeping this module importable avoids crashes from the
old Qt4 resource payload while pyrcc5 is not available.
"""


def qInitResources():
    pass


def qCleanupResources():
    pass
