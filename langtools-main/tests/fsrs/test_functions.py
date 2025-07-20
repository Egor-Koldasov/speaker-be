"""Tests for FSRS functions."""

import unittest
from datetime import datetime, timedelta, timezone
from typing import cast

from langtools.main.fsrs import FSRSCardState, Rating, new_training_data, process_review


class TestFSRSFunctions(unittest.TestCase):
    """Test FSRS functions."""

    def test_new_training_data(self):
        """Test creation of initial training data."""
        training_data = new_training_data()

        # Should be in LEARNING state (new cards start learning)
        self.assertEqual(training_data.state, FSRSCardState.LEARNING)

        # Should have initial values
        self.assertEqual(training_data.reps, 0)
        self.assertEqual(training_data.lapses, 0)
        self.assertIsNone(training_data.last_review)
        self.assertEqual(training_data.step, 0)

        # Should have None stability and difficulty for new cards
        self.assertIsNone(training_data.stability)
        self.assertIsNone(training_data.difficulty)

        # Should be due immediately or very soon
        now = datetime.now(timezone.utc)
        self.assertLessEqual(training_data.due, now + timedelta(minutes=1))

    def test_process_review_good(self):
        """Test processing a successful review."""
        training_data = new_training_data()
        review_time = datetime.now(timezone.utc)

        updated_data = process_review(training_data, Rating.GOOD, review_time)

        # Should increment reps
        self.assertEqual(updated_data.reps, 1)

        # Should set last_review
        self.assertEqual(updated_data.last_review, review_time)

        # Should have stability and difficulty now
        self.assertIsNotNone(updated_data.stability)
        self.assertIsNotNone(updated_data.difficulty)

        # Should stay in learning or move to review state
        self.assertIn(updated_data.state, [FSRSCardState.LEARNING, FSRSCardState.REVIEW])

    def test_process_review_again(self):
        """Test processing a failed review."""
        training_data = new_training_data()
        review_time = datetime.now(timezone.utc)

        updated_data = process_review(training_data, Rating.AGAIN, review_time)

        # Should increment lapses
        self.assertEqual(updated_data.lapses, 1)

        # Should set last_review
        self.assertEqual(updated_data.last_review, review_time)

        # Should be in learning or relearning state
        self.assertIn(updated_data.state, [FSRSCardState.LEARNING, FSRSCardState.RELEARNING])

    def test_process_review_hard(self):
        """Test processing a hard review."""
        training_data = new_training_data()
        review_time = datetime.now(timezone.utc)

        updated_data = process_review(training_data, Rating.HARD, review_time)

        # Should increment reps
        self.assertEqual(updated_data.reps, 1)

        # Should set last_review
        self.assertEqual(updated_data.last_review, review_time)

    def test_process_review_easy(self):
        """Test processing an easy review."""
        training_data = new_training_data()
        review_time = datetime.now(timezone.utc)

        updated_data = process_review(training_data, Rating.EASY, review_time)

        # Should increment reps
        self.assertEqual(updated_data.reps, 1)

        # Should set last_review
        self.assertEqual(updated_data.last_review, review_time)

        # Should have due date in the future
        self.assertGreater(updated_data.due, review_time)

    def test_process_review_invalid_rating(self):
        """Test that invalid rating raises ValueError."""
        training_data = new_training_data()
        review_time = datetime.now(timezone.utc)

        with self.assertRaises(ValueError):
            process_review(training_data, cast(Rating, 0), review_time)  # Too low

        with self.assertRaises(ValueError):
            process_review(training_data, cast(Rating, 5), review_time)  # Too high

    def test_process_review_sequence(self):
        """Test a sequence of reviews."""
        training_data = new_training_data()

        # First review - GOOD
        review_time_1 = datetime.now(timezone.utc)
        training_data = process_review(training_data, Rating.GOOD, review_time_1)

        self.assertEqual(training_data.reps, 1)
        self.assertEqual(training_data.lapses, 0)

        # Second review - AGAIN (forgot)
        review_time_2 = review_time_1 + timedelta(days=1)
        training_data = process_review(training_data, Rating.AGAIN, review_time_2)

        self.assertEqual(training_data.reps, 2)
        self.assertEqual(training_data.lapses, 1)

        # Third review - EASY
        review_time_3 = review_time_2 + timedelta(hours=1)
        training_data = process_review(training_data, Rating.EASY, review_time_3)

        self.assertEqual(training_data.reps, 3)
        self.assertEqual(training_data.lapses, 1)

    def test_due_date_progression(self):
        """Test that due dates progress correctly."""
        training_data = new_training_data()
        review_time = datetime.now(timezone.utc)

        # After a GOOD review, due date should be in the future
        updated_data = process_review(training_data, Rating.GOOD, review_time)
        self.assertGreater(updated_data.due, review_time)

        # After an EASY review, due date should be even further in the future
        easy_data = process_review(training_data, Rating.EASY, review_time)
        self.assertGreaterEqual(easy_data.due, updated_data.due)


if __name__ == "__main__":
    unittest.main()
