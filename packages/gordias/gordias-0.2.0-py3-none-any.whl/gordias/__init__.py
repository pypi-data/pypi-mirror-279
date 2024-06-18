# -*- coding: utf-8 -*-

from importlib.metadata import version, PackageNotFoundError


try:
    __version__ = version("gordias")
except PackageNotFoundError as e:
    raise PackageNotFoundError("Gordias package could not be found.") from e
