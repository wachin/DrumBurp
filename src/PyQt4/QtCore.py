from PyQt5.QtCore import *  # noqa
try:
    from PyQt5.QtCore import pyqtSignal, pyqtSlot, pyqtProperty
except Exception:  # pragma: no cover
    pass

def pyqtSignature(signature="", *args, **kwargs):
    type_map = {"int": int, "bool": bool, "QString": str, "str": str}
    signature = str(signature)
    if not signature:
        return pyqtSlot()
    slot_types = [type_map.get(item.strip(), object)
                  for item in signature.split(",")
                  if item.strip()]
    return pyqtSlot(*slot_types)

_QT5_QSETTINGS = QSettings

class _CompatVariant:
    def __init__(self, value=None):
        self.value = value

    def toString(self):
        return "" if self.value is None else str(self.value)

    def toStringList(self):
        if self.value is None:
            return []
        if isinstance(self.value, (list, tuple)):
            return [str(item) for item in self.value]
        return [str(self.value)]

    def toBool(self):
        if isinstance(self.value, str):
            return self.value.lower() in ("1", "true", "yes", "on")
        return bool(self.value)

    def toByteArray(self):
        if self.value is None:
            return QByteArray()
        return self.value

    def toInt(self):
        try:
            return int(self.value), True
        except (TypeError, ValueError):
            return 0, False

    def __bool__(self):
        return self.toBool()

    def __str__(self):
        return self.toString()

    def __getattr__(self, name):
        return getattr(self.value, name)

def QVariant(value=None):
    return _CompatVariant(value)

class QSettings(_QT5_QSETTINGS):
    def value(self, key, defaultValue=None, type=None):
        if type is None:
            value = super(QSettings, self).value(key, defaultValue)
        else:
            value = super(QSettings, self).value(key, defaultValue, type=type)
        return _CompatVariant(value)

def SIGNAL(signature):
    return signature

def SLOT(signature):
    return signature

def _signal_name(signature):
    signature = str(signature)
    return signature.split("(", 1)[0]

def _signal_args(signature):
    signature = str(signature)
    if "(" not in signature:
        return ""
    return signature.split("(", 1)[1].rsplit(")", 1)[0]

def _old_style_connect(sender, signal, receiver):
    bound_signal = getattr(sender, _signal_name(signal))
    args = _signal_args(signal)
    overloads = {"int": int, "bool": bool, "QString": str, "str": str}
    if args in overloads:
        try:
            bound_signal = bound_signal[overloads[args]]
        except (KeyError, TypeError):
            pass
    bound_signal.connect(receiver)

try:
    QObject.connect = staticmethod(_old_style_connect)
except Exception:
    pass

class QString(str):
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
