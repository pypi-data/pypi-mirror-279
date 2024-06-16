# tests/test_config.py

import os
import pytest
from ponfig import get_config

def test_get_config(monkeypatch):
    monkeypatch.setattr(os, 'getcwd', lambda: os.path.join(os.path.dirname(__file__), 'test_project'))
    assert get_config('app.example') == 'example_value'