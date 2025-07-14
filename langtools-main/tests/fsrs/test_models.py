"""Tests for FSRS models."""

import unittest
from datetime import datetime, timezone

from langtools.main.fsrs.models import FSRSCardState, FSRSTrainingData, Rating


class TestFSRSModels(unittest.TestCase):
    """Test FSRS data models."""

    def test_fsrs_card_state_enum(self):
        """Test FSRSCardState enum values."""
        self.assertEqual(FSRSCardState.LEARNING, 1)
        self.assertEqual(FSRSCardState.REVIEW, 2)
        self.assertEqual(FSRSCardState.RELEARNING, 3)

    def test_rating_enum(self):
        """Test Rating enum values."""
        self.assertEqual(Rating.AGAIN, 1)
        self.assertEqual(Rating.HARD, 2)
        self.assertEqual(Rating.GOOD, 3)
        self.assertEqual(Rating.EASY, 4)

    def test_fsrs_training_data_creation(self):
        """Test FSRSTrainingData dataclass creation."""
        now = datetime.now(timezone.utc)

        training_data = FSRSTrainingData(
            due=now,
            stability=None,
            difficulty=None,
            state=FSRSCardState.LEARNING,
            step=0,
            last_review=None,
            reps=0,
            lapses=0,
        )

        self.assertEqual(training_data.due, now)
        self.assertIsNone(training_data.stability)
        self.assertIsNone(training_data.difficulty)
        self.assertEqual(training_data.state, FSRSCardState.LEARNING)
        self.assertEqual(training_data.step, 0)
        self.assertEqual(training_data.reps, 0)
        self.assertEqual(training_data.lapses, 0)
        self.assertIsNone(training_data.last_review)

    def test_fsrs_training_data_mutability(self):
        """Test that FSRSTrainingData is mutable."""
        now = datetime.now(timezone.utc)

        training_data = FSRSTrainingData(
            due=now,
            stability=None,
            difficulty=None,
            state=FSRSCardState.LEARNING,
            step=0,
        )

        # Should be able to modify fields
        training_data.reps = 1
        training_data.state = FSRSCardState.LEARNING
        training_data.last_review = now
        training_data.stability = 2.0
        training_data.difficulty = 5.0

        self.assertEqual(training_data.reps, 1)
        self.assertEqual(training_data.state, FSRSCardState.LEARNING)
        self.assertEqual(training_data.last_review, now)
        self.assertEqual(training_data.stability, 2.0)
        self.assertEqual(training_data.difficulty, 5.0)


if __name__ == "__main__":
    unittest.main()
