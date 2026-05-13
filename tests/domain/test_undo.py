"""Tests for snapshot history helpers."""

from __future__ import annotations

import pytest

from nardy.domain.rules_long import LongNardyRules
from nardy.domain.undo import SnapshotStore, UndoUnavailableError


def test_snapshot_store_push_pop_and_clear() -> None:
    """Snapshot store should behave like a simple LIFO history."""
    first = LongNardyRules().initial_state()
    second = first.switch_player()
    store = SnapshotStore([first])

    assert store.can_undo() is True

    store.push(second)

    assert store.pop() == second
    assert store.pop() == first
    assert store.can_undo() is False

    store.push(first)
    store.clear()

    assert store.can_undo() is False


def test_snapshot_store_rejects_pop_without_history() -> None:
    """Popping an empty history should raise a domain error."""
    store = SnapshotStore()

    with pytest.raises(UndoUnavailableError, match="No snapshots"):
        store.pop()
