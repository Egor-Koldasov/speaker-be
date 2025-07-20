"""FSRS functions for spaced repetition training data management."""

from datetime import datetime, timedelta

from fsrs import Card as PyFSRSCard
from fsrs import Rating as PyFSRSRating
from fsrs import Scheduler as PyFSRSScheduler
from fsrs import State as PyFSRSState

from .models import FSRSCardState, FSRSTrainingData, Rating

# Global scheduler instance with default parameters
_DEFAULT_SCHEDULER = PyFSRSScheduler(
    desired_retention=0.90,
    learning_steps=[timedelta(minutes=1), timedelta(minutes=10)],  # 1 min, 10 min
    relearning_steps=[timedelta(minutes=10)],  # 10 min for failed cards
    enable_fuzzing=True,
)


def new_training_data() -> FSRSTrainingData:
    """
    Create initial FSRS training data for a new learning item.

    Returns:
        FSRSTrainingData: Initial training data ready for first review
    """
    # Create new py-fsrs card to get initial parameters
    py_card = PyFSRSCard()

    return FSRSTrainingData(
        due=py_card.due,
        stability=py_card.stability,  # None for new cards
        difficulty=py_card.difficulty,  # None for new cards
        state=FSRSCardState(py_card.state.value),
        step=py_card.step if py_card.step is not None else 0,
        last_review=py_card.last_review,  # None for new cards
        reps=0,
        lapses=0,
    )


def process_review(
    training_data: FSRSTrainingData, rating: Rating, review_time: datetime
) -> FSRSTrainingData:
    """
    Process a review session and return updated training data.

    Args:
        training_data: Current FSRS training state
        rating: Review rating (Again/Hard/Good/Easy)
        review_time: When review occurred

    Returns:
        FSRSTrainingData: Updated training data

    Raises:
        ValueError: If rating is invalid
    """
    if rating not in [Rating.AGAIN, Rating.HARD, Rating.GOOD, Rating.EASY]:
        raise ValueError(f"Invalid rating: {rating}. Must be 1-4.")

    # Convert to py-fsrs objects
    py_card = _to_py_card(training_data)
    py_rating = PyFSRSRating(rating.value)

    # Process review
    updated_py_card, _ = _DEFAULT_SCHEDULER.review_card(py_card, py_rating, review_time)

    # Convert back to our training data with updated counters
    new_reps = training_data.reps + 1
    new_lapses = training_data.lapses + (1 if rating == Rating.AGAIN else 0)

    return FSRSTrainingData(
        due=updated_py_card.due,
        stability=updated_py_card.stability,
        difficulty=updated_py_card.difficulty,
        state=FSRSCardState(updated_py_card.state.value),
        step=updated_py_card.step if updated_py_card.step is not None else 0,
        last_review=updated_py_card.last_review,
        reps=new_reps,
        lapses=new_lapses,
    )


def _to_py_card(training_data: FSRSTrainingData) -> PyFSRSCard:
    """Convert FSRSTrainingData to py-fsrs Card."""
    card = PyFSRSCard()
    card.due = training_data.due
    card.stability = training_data.stability
    card.difficulty = training_data.difficulty
    card.state = PyFSRSState(training_data.state.value)
    card.step = training_data.step
    card.last_review = training_data.last_review
    return card
