"""Ruleset skeleton for long backgammon."""

from __future__ import annotations

from typing import Mapping

from nardy.domain.models import BOARD_POINT_COUNT, GameMode, GameState, Player
from nardy.domain.rules_base import BaseRuleset


class LongNardyRules(BaseRuleset):
    """Partial implementation of the long backgammon rules contract."""

    mode = GameMode.LONG

    def initial_layout(self) -> Mapping[int, tuple[Player, int]]:
        """Return the starting positions for long backgammon."""
        return {
            24: (Player.WHITE, 15),
            12: (Player.BLACK, 15),
        }

    def direction_for(self, player: Player) -> int:
        """Return the movement direction for a player."""
        del player
        return -1

    def target_for(self, player: Player, source: int, die_value: int) -> int | None:
        """Return target point along the player's circular movement path."""
        path = self._path_for(player)
        index = path.index(source) + die_value
        if index >= BOARD_POINT_COUNT:
            return None
        return path[index]

    def home_points_for(self, player: Player) -> range:
        """Return the player's home board points."""
        if player is Player.WHITE:
            return range(1, 7)
        return range(13, 19)

    def _is_exact_bear_off(
        self,
        player: Player,
        source: int,
        die_value: int,
    ) -> bool:
        """Return ``True`` when die reaches the end of the movement path."""
        path = self._path_for(player)
        return path.index(source) + die_value == BOARD_POINT_COUNT

    def _can_bear_off_with_overshoot(
        self,
        state: GameState,
        player: Player,
        source: int,
    ) -> bool:
        """Allow overshoot only from the farthest occupied home point."""
        path = self._path_for(player)
        source_index = path.index(source)
        return not any(
            state.point(point).owner is player and state.point(point).checkers > 0
            for point in self.home_points_for(player)
            if path.index(point) < source_index
        )

    def can_land_on_point(
        self,
        state: GameState,
        player: Player,
        point_number: int,
    ) -> bool:
        """Allow landing only on empty or friendly points."""
        point = state.point(point_number)
        return point.owner in (None, player)

    @staticmethod
    def _path_for(player: Player) -> tuple[int, ...]:
        """Return board points in movement order for the player."""
        if player is Player.WHITE:
            return tuple(range(24, 0, -1))
        return tuple(range(12, 0, -1)) + tuple(range(24, 12, -1))
