"""Application bootstrap helpers."""

from __future__ import annotations

import argparse

from nardy import __version__


def build_parser() -> argparse.ArgumentParser:
    """Create the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="nardy",
        description="Run the Nardy application.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Console entry point used by the project script."""
    parser = build_parser()
    parser.parse_args(argv)
    return 0
