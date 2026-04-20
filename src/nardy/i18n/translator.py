"""Translation helpers backed by gettext catalogs."""

from __future__ import annotations

import gettext
from pathlib import Path


def gettext_noop(message: str) -> str:
    """Mark a string for translation without translating it immediately."""
    return message


class Localizer:
    """Provide gettext-based message translation for the application."""

    def __init__(self, locale_code: str = "en", domain: str = "nardy") -> None:
        """Initialize the translator for a locale code."""
        self._locale_code = locale_code
        self._domain = domain
        self._translation = gettext.translation(
            domain=domain,
            localedir=self._locale_dir(),
            languages=[locale_code],
            fallback=True,
        )

    @staticmethod
    def _locale_dir() -> Path:
        """Return the locale directory bundled with the package."""
        return Path(__file__).with_name("locale")

    @property
    def locale_code(self) -> str:
        """Return the currently active locale code."""
        return self._locale_code

    def gettext(self, message: str) -> str:
        """Translate a message using the active catalog."""
        return self._translation.gettext(message)

    __call__ = gettext
