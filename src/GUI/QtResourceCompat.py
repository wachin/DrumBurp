import os

from PyQt5.QtGui import QPixmap as _QPixmap


_SRC_DIR = os.path.dirname(os.path.dirname(__file__))


def resourcePath(path):
    if not isinstance(path, str) or not path.startswith(":/"):
        return path
    resource = path[2:]
    if resource.startswith("Icons/Icons/"):
        resource = "GUI/Icons/" + resource[len("Icons/Icons/"):]
    elif resource.startswith("Icons/"):
        resource = "GUI/" + resource
    elif resource.startswith("buttons/GUI/"):
        resource = resource[len("buttons/"):]
    elif resource.startswith("heads/GUI/"):
        resource = resource[len("heads/"):]
    return os.path.join(_SRC_DIR, resource)


def QPixmap(*args):
    if args:
        args = (resourcePath(args[0]),) + args[1:]
    return _QPixmap(*args)
