import random
from typing import Dict, List
from django.db import transaction
from .models import GameSession

#Available symbols
SYMBOLS: List[str] = ["cherry", "lemon", "orange", "watermelon"]

#Reward Mapping
REWARDS: Dict[str, int] = {
    "cherry": 10,
    "lemon": 20,
    "orange": 30,
    "watermelon": 40,
}

SPIN_COST: int = 1


def should_reroll(credits: int) -> bool:
    """
    Determine whether a winning spin should be rerolled based on current credits.
    """
    if credits < 40:
        return False
    elif 40 <= credits <= 60:
        return random.random() < 0.3
    return random.random() < 0.6


def generate_symbols() -> List[str]:
    """
    Generate a list of three random slot symbols.
    """
    return [random.choice(SYMBOLS) for _ in range(3)]


def calculate_reward(symbols: List[str]) -> int:
    """
    Return reward if all symbols match, otherwise 0.
    """
    if symbols and len(set(symbols)) == 1:
        return REWARDS[symbols[0]]
    return 0

@transaction.atomic
def spin_game(session: GameSession) -> Dict[str, object]:
    """
    Execute a single spin for a game session.

    Deducts credits, generates symbols, applies reward and reroll logic,
    and updates session state.
    """

    #Ensure session has credits
    if session.credits <= 0:
        session.is_active = False
        session.save()
        raise ValueError("Not enough credits to perform spin.")

    # Deduct spin cost
    session.credits -= SPIN_COST

    symbols = generate_symbols()
    reward = calculate_reward(symbols)
    is_win = reward > 0

    # Apply reroll logic
    if is_win and should_reroll(session.credits):
        symbols = generate_symbols()
        reward = calculate_reward(symbols)
        is_win = reward > 0

    # Update credits
    session.credits += reward

    # End session if no credits left
    if session.credits <= 0:
        session.is_active = False

    session.save()

    return {
        "symbols": symbols,
        "is_win": is_win,
        "reward": reward,
        "credits": session.credits,
    }