# Copyright (c) 2024, qBraid Development Team
# All rights reserved.

"""
Module defining qBraid service clients.

.. currentmodule:: qbraid_core.services

"""
__all__ = []

_lazy_mods = ["admin", "environments", "quantum"]


def __getattr__(name):
    if name in _lazy_mods:
        import importlib  # pylint: disable=import-outside-toplevel

        module = importlib.import_module(f".{name}", __name__)
        globals()[name] = module
        return module
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def __dir__():
    return sorted(__all__ + _lazy_mods)
