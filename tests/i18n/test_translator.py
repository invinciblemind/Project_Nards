"""Tests for gettext-based localization helpers."""

from __future__ import annotations

from nardy.i18n import Localizer, gettext_noop


def test_gettext_noop_returns_same_message() -> None:
    """The noop marker should preserve the source message."""
    assert gettext_noop("Nardy") == "Nardy"


def test_localizer_falls_back_to_source_message_for_unknown_locale() -> None:
    """The localizer should gracefully fall back for an unknown locale."""
    localizer = Localizer(locale_code="zz")
    assert localizer.gettext("Nardy") == "Nardy"
