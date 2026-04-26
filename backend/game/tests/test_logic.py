import pytest
from unittest.mock import patch

from game.services import (
    calculate_reward,
    generate_symbols,
    should_reroll,
    spin_game,
    cashout_session
)
from game.models import GameSession
from django.contrib.auth import get_user_model

User = get_user_model()
# PURE LOGIC TESTS

def test_calculate_reward_cherry():
    symbols = ["cherry", "cherry", "cherry"]
    assert calculate_reward(symbols) == 10


def test_calculate_reward_lemon():
    symbols = ["lemon", "lemon", "lemon"]
    assert calculate_reward(symbols) == 20


def test_calculate_reward_no_match():
    symbols = ["cherry", "lemon", "orange"]
    assert calculate_reward(symbols) == 0


def test_generate_symbols_length():
    symbols = generate_symbols()
    assert len(symbols) == 3


def test_generate_symbols_valid_values():
    symbols = generate_symbols()
    valid = ["cherry", "lemon", "orange", "watermelon"]

    for symbol in symbols:
        assert symbol in valid


# MOCKING RANDOMNESS


def test_generate_symbols_mocked():
    with patch("game.services.random.choice", return_value="cherry"):
        symbols = generate_symbols()

        assert symbols == ["cherry", "cherry", "cherry"]


def test_should_reroll_below_40():
    assert should_reroll(30) is False


def test_should_reroll_returns_boolean():
    result = should_reroll(50)
    assert result in [True, False]


# SERVICE TESTS (DB REQUIRED)

@pytest.mark.django_db
def test_spin_game_reduces_or_updates_credits():
    user = User.objects.create_user(username="test", password="pass")
    session = GameSession.objects.create(user=user, credits=10)

    result = spin_game(session)

    assert "symbols" in result
    assert "credits" in result
    assert len(result["symbols"]) == 3
    assert result["credits"] >= 0


@pytest.mark.django_db
def test_spin_game_with_mocked_symbols_win():
    user = User.objects.create_user(username="test", password="pass")
    session = GameSession.objects.create(user=user, credits=10)

    with patch("game.services.generate_symbols", return_value=["cherry", "cherry", "cherry"]):
        result = spin_game(session)

        assert result["is_win"] is True
        assert result["reward"] == 10


@pytest.mark.django_db
def test_spin_game_ends_session_when_no_credits():
    user = User.objects.create_user(username="test", password="pass")
    session = GameSession.objects.create(user=user, credits=0)

    with pytest.raises(ValueError):
        spin_game(session)

    session.refresh_from_db()
    assert session.credits <= 0


@pytest.mark.django_db
def test_cashout_transfers_balance():
    user = User.objects.create_user(username="test", password="pass", wallet_balance=0)
    session = GameSession.objects.create(user=user, credits=20)

    result = cashout_session(session)

    user.refresh_from_db()
    session.refresh_from_db()

    assert result["cashed_out"] == 20
    assert user.wallet_balance == 20
    assert session.credits == 0
    assert session.is_active is False


@pytest.mark.django_db
def test_cashout_no_credits_raises_error():
    user = User.objects.create_user(username="test", password="pass", wallet_balance=0)
    session = GameSession.objects.create(user=user, credits=0)

    with pytest.raises(ValueError):
        cashout_session(session)