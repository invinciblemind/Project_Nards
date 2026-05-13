"""Tests for pure application presentation helpers."""

from __future__ import annotations

from dataclasses import replace

from nardy.app import presentation
from nardy.app.presentation import present_game_state, present_victory
from nardy.domain.models import DiceRoll, Player, TurnPhase
from nardy.domain.rules_long import LongNardyRules
from nardy.i18n import Localizer


def test_present_game_state_exposes_mode_and_action_hint() -> None:
    """The game presenter should provide compact labels for the screen."""
    localizer = Localizer()
    state = LongNardyRules().initial_state()

    data = present_game_state(localizer, state=state, can_undo=False)

    assert data.subtitle == "Mode: Long backgammon"
    assert data.status == "White: roll dice."
    assert data.can_roll is True
    assert data.can_undo is False


def test_present_victory_formats_the_winner_message() -> None:
    """The victory presenter should include the translated winner name."""
    localizer = Localizer()
    state = replace(LongNardyRules().initial_state(), winner=Player.WHITE)

    data = present_victory(localizer, state)

    assert data.title == "Victory"
    assert data.summary == "White wins."


def test_present_game_state_shows_ready_phase_and_remaining_dice() -> None:
    """Ready phase should ask for a checker and render remaining dice."""
    localizer = Localizer()
    state = LongNardyRules().initial_state()
    turn = state.turn.with_roll(DiceRoll.from_values(3, 5))
    turn = replace(
        turn,
        remaining_pips=(5,),
        phase=TurnPhase.READY_TO_MOVE,
    )
    state = replace(state, turn=turn)

    data = present_game_state(localizer, state=state, can_undo=True)

    assert data.status == "White: choose a highlighted checker."
    assert data.dice == "Dice: 3,5 [5]"
    assert data.can_roll is False
    assert data.can_undo is True


def test_present_game_state_shows_finished_phase_empty_dice_and_override() -> None:
    """Finished phase and explicit status overrides should be rendered."""
    localizer = Localizer()
    state = LongNardyRules().initial_state()
    finished_turn = replace(
        state.turn.with_roll(DiceRoll.from_values(1, 2)),
        phase=TurnPhase.TURN_COMPLETE,
        remaining_pips=(),
    )
    state = replace(state, turn=finished_turn)

    finished = present_game_state(localizer, state=state, can_undo=False)
    overridden = present_game_state(
        localizer,
        state=state,
        can_undo=False,
        status_override="Custom status",
    )

    assert finished.status == "White: turn finished."
    assert finished.dice == "Dice: 1,2 [-]"
    assert overridden.status == "Custom status"


def test_present_victory_falls_back_to_current_player() -> None:
    """Victory presenter should use current player when winner is absent."""
    localizer = Localizer()
    state = LongNardyRules().initial_state().switch_player()

    data = present_victory(localizer, state)

    assert data.summary == "Black wins."


def test_player_label_handles_missing_player() -> None:
    """Unknown players should have a fallback presentation label."""
    assert presentation._player_label(None) == "Unknown player"
