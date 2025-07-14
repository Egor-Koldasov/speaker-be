"""FSRS data models for spaced repetition training data."""

from dataclasses import dataclass
from datetime import datetime
from enum import IntEnum


class FSRSCardState(IntEnum):
    """FSRS card learning states."""

    LEARNING = 1
    REVIEW = 2
    RELEARNING = 3


class Rating(IntEnum):
    """Review rating values."""

    AGAIN = 1  # Forgot the card
    HARD = 2  # Remembered with serious difficulty
    GOOD = 3  # Remembered after a hesitation
    EASY = 4  # Remembered easily


@dataclass
class FSRSTrainingData:
    """
    FSRS training data for a learning item.

    Attributes:
        due: When the next review is due
        stability: Memory stability (days) - None for new cards
        difficulty: Learning difficulty (0-10) - None for new cards
        state: Current card state
        step: Current learning step
        last_review: When last reviewed (optional)
        reps: Number of reviews (tracked separately)
        lapses: Number of failed reviews (tracked separately)
    """

    due: datetime
    stability: float | None
    difficulty: float | None
    state: FSRSCardState
    step: int
    last_review: datetime | None = None
    reps: int = 0
    lapses: int = 0
