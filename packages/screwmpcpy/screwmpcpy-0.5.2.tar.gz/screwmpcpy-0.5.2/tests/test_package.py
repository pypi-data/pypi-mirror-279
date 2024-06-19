from __future__ import annotations

import importlib.metadata

import screwmpcpy as m


def test_version():
    assert importlib.metadata.version("screwmpcpy") == m.__version__
