"""Sphinx configuration for the Nardy project."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

project = "Nardy"
author = "Nardy Team"
copyright = "2026, Nardy Team"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.napoleon",
]

autosummary_generate = True
templates_path = ["_templates"]
exclude_patterns = ["_build"]
language = "ru"
html_theme = "alabaster"
