"""Tests for module execution entry point."""

from __future__ import annotations

import runpy

import pytest


def test_main_module_exits_with_bootstrap_status(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Running ``python -m nardy`` should delegate to bootstrap main."""
    monkeypatch.setattr("nardy.app.bootstrap.main", lambda: 7)

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_module("nardy.__main__", run_name="__main__")

    assert exc_info.value.code == 7
