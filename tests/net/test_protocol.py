"""Tests for the future networking seam."""

from __future__ import annotations

from nardy.net import MessageKind, NetworkEnvelope


def test_network_envelope_preserves_message_kind_and_payload() -> None:
    """The envelope should expose the transport metadata unchanged."""
    envelope = NetworkEnvelope(
        kind=MessageKind.PLAYER_ACTION,
        payload={"move": "24-23"},
    )

    assert envelope.kind is MessageKind.PLAYER_ACTION
    assert envelope.payload["move"] == "24-23"
