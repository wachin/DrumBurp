from PyQt5.QtCore import *  # noqa
try:
    from PyQt5.QtCore import pyqtSignal, pyqtSlot, pyqtProperty
except Exception:  # pragma: no cover
    pass

def pyqtSignature(*args, **kwargs):
    def decorator(func):
        return func
    return decorator

def QVariant(value=None):
    return value

class QString:
    @staticmethod
    def fromUtf8(value):
        return value

# PyQt4 .qrc files generated Python 2 strings. PyQt5 on Python 3 wants bytes.
try:
    _orig_qRegisterResourceData = qRegisterResourceData
    _orig_qUnregisterResourceData = qUnregisterResourceData
    def _as_bytes(value):
        return value.encode('latin1') if isinstance(value, str) else value
    def qRegisterResourceData(version, tree, name, data):
        return _orig_qRegisterResourceData(version, _as_bytes(tree), _as_bytes(name), _as_bytes(data))
    def qUnregisterResourceData(version, tree, name, data):
        return _orig_qUnregisterResourceData(version, _as_bytes(tree), _as_bytes(name), _as_bytes(data))
except Exception:
    pass
