# tests/test_env.py

import os
import pytest
from ponfig import get_env

def test_get_env(monkeypatch):
    monkeypatch.setattr(os, 'getcwd', lambda: os.path.join(os.path.dirname(__file__), 'test_project'))
    assert get_env('app.example') == 'example_value'