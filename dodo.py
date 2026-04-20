"""Project automation tasks powered by doit."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

DOIT_CONFIG = {
    "default_tasks": ["check"],
}

ROOT = Path(__file__).parent.resolve()


def _run(*args: str) -> bool:
    """Execute a Python-based command in the project root."""
    completed = subprocess.run(
        [sys.executable, *args],
        cwd=ROOT,
        check=False,
    )
    return completed.returncode == 0


def task_lint() -> dict[str, object]:
    """Run code quality checks."""
    return {
        "actions": [
            (_run, ("-m", "flake8", "src", "tests", "dodo.py", "docs/conf.py")),
            (_run, ("-m", "pydocstyle", "src", "tests", "dodo.py")),
        ],
        "verbosity": 2,
    }


def task_test() -> dict[str, object]:
    """Run the test suite."""
    return {
        "actions": [
            (_run, ("-m", "pytest")),
        ],
        "verbosity": 2,
    }


def task_coverage() -> dict[str, object]:
    """Run tests with coverage reporting."""
    return {
        "actions": [
            (
                _run,
                (
                    "-m",
                    "pytest",
                    "--cov=nardy",
                    "--cov-report=term-missing",
                    "--cov-report=xml",
                ),
            ),
        ],
        "verbosity": 2,
    }


def task_docs() -> dict[str, object]:
    """Build project documentation."""
    return {
        "actions": [
            (_run, ("-m", "sphinx", "-b", "html", "docs", "docs/_build/html")),
        ],
        "verbosity": 2,
    }


def task_build() -> dict[str, object]:
    """Create source and wheel distributions."""
    return {
        "actions": [
            (_run, ("-m", "build")),
        ],
        "verbosity": 2,
    }


def task_babel_extract() -> dict[str, object]:
    """Extract translatable strings into the catalog template."""
    return {
        "actions": [
            (
                _run,
                (
                    "-m",
                    "babel.messages.frontend",
                    "extract",
                    "-F",
                    "babel.cfg",
                    "-o",
                    "src/nardy/i18n/locale/messages.pot",
                    "src",
                ),
            ),
        ],
        "verbosity": 2,
    }


def task_babel_update() -> dict[str, object]:
    """Update locale catalogs from the extracted template."""
    return {
        "actions": [
            (
                _run,
                (
                    "-m",
                    "babel.messages.frontend",
                    "update",
                    "-D",
                    "nardy",
                    "-i",
                    "src/nardy/i18n/locale/messages.pot",
                    "-d",
                    "src/nardy/i18n/locale",
                ),
            ),
        ],
        "verbosity": 2,
        "task_dep": ["babel_extract"],
    }


def task_babel_compile() -> dict[str, object]:
    """Compile locale catalogs into binary gettext files."""
    return {
        "actions": [
            (
                _run,
                (
                    "-m",
                    "babel.messages.frontend",
                    "compile",
                    "-D",
                    "nardy",
                    "-d",
                    "src/nardy/i18n/locale",
                ),
            ),
        ],
        "verbosity": 2,
    }


def task_check() -> dict[str, object]:
    """Run the standard verification pipeline."""
    return {
        "actions": None,
        "task_dep": [
            "lint",
            "test",
            "coverage",
            "docs",
            "babel_extract",
            "babel_update",
            "babel_compile",
            "build",
        ],
    }
