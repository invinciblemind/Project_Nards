"""Networking contracts reserved for the future LAN implementation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Protocol


class MessageKind(str, Enum):
    """Enumerate the transport-level message categories."""

    GAME_STATE = "game_state"
    PLAYER_ACTION = "player_action"
    CONTROL = "control"


@dataclass(frozen=True, slots=True)
class NetworkEnvelope:
    """Wrap a transport payload with a stable message kind."""

    kind: MessageKind
    payload: Mapping[str, Any]


class Transport(Protocol):
    """Describe the minimal contract expected from a network transport."""

    def send(self, envelope: NetworkEnvelope) -> None:
        """Send one serialized domain-related message."""

    def receive(self) -> NetworkEnvelope | None:
        """Return the next available message, if any."""

    def close(self) -> None:
        """Release transport resources and terminate the session."""
