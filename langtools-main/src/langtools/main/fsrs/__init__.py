"""FSRS training data management module.

This module provides simple functional API for spaced repetition training data:
- new_training_data(): Create initial training data for new learning items
- process_review(): Update training data based on review performance

Example usage:
    from langtools.main.fsrs import new_training_data, process_review, Rating
    from datetime import datetime, timezone

    # Create new training data
    training_data = new_training_data()

    # Process a review
    review_time = datetime.now(timezone.utc)
    training_data = process_review(training_data, Rating.GOOD, review_time)
"""

from .functions import new_training_data, process_review
from .models import FSRSCardState, FSRSTrainingData, Rating

__all__ = [
    "new_training_data",
    "process_review",
    "FSRSTrainingData",
    "FSRSCardState",
    "Rating",
]
