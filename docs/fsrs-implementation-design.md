# FSRS Training Data Management - Design Specification

## Overview

This document outlines the design and implementation of pure FSRS (Free Spaced Repetition Scheduler) training data management within the `langtools-main` package. The implementation provides core spaced repetition scheduling functionality using the `py-fsrs` package as a functional library, focusing solely on:

1. **Creating initial training data for new cards** - Initialize FSRS state
2. **Processing reviews and updating training data** - Update scheduling parameters based on review performance

This module is content-agnostic and provides pure functional scheduling logic that can be used by any learning application.

## Architecture Overview

### Package Location
```
langtools-main/
├── src/
│   └── langtools/
│       └── main/
│           └── fsrs/           # Pure FSRS module
│               ├── __init__.py
│               ├── models.py   # FSRS data models
│               └── functions.py # FSRS functional API
└── tests/
    └── fsrs/                   # FSRS tests
        ├── test_models.py
        └── test_functions.py
```

### Design Principles

1. **Functional Approach**: Pure functions with no classes or state
2. **Content Agnostic**: No knowledge of what is being learned (vocabulary, images, etc.)
3. **Storage Agnostic**: No persistence logic - pure data transformation
4. **Simple Data Structures**: Plain dataclasses without complexity

## Core Components

### 1. FSRS Data Models (`fsrs/models.py`)

Simple data structures for FSRS scheduling state.

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import IntEnum

class FSRSCardState(IntEnum):
    """FSRS card learning states."""
    NEW = 0
    LEARNING = 1  
    REVIEW = 2
    RELEARNING = 3

class Rating(IntEnum):
    """Review rating values."""
    AGAIN = 1    # Forgot the card
    HARD = 2     # Remembered with serious difficulty
    GOOD = 3     # Remembered after a hesitation  
    EASY = 4     # Remembered easily

@dataclass
class FSRSTrainingData:
    """
    FSRS training data state - content agnostic.
    Represents all scheduling parameters for a single learning item.
    """
    # Core scheduling parameters
    due: datetime                    # When the card is next due for review
    stability: float                 # Current memory stability
    difficulty: float                # Item difficulty (0.0 to 10.0)
    
    # Learning progress
    elapsed_days: int                # Days since last review
    scheduled_days: int              # Days scheduled for next review 
    reps: int                        # Total number of reviews
    lapses: int                      # Number of times forgotten
    state: FSRSCardState             # Current learning state
    last_review: Optional[datetime] = None  # When last reviewed
```

### 2. FSRS Functions (`fsrs/functions.py`)

Simple functional API with only 2 essential functions.

```python
from fsrs import Scheduler as PyFSRSScheduler, Card as PyFSRSCard, Rating as PyFSRSRating, State as PyFSRSState
from datetime import datetime
from .models import FSRSTrainingData, FSRSCardState, Rating

# Global scheduler instance with default parameters
_DEFAULT_SCHEDULER = PyFSRSScheduler(
    desired_retention=0.90,
    learning_steps=[1, 10],      # 1 min, 10 min for new cards
    relearning_steps=[10],       # 10 min for failed cards
    enable_fuzzing=True
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
        stability=py_card.stability,
        difficulty=py_card.difficulty,
        elapsed_days=py_card.elapsed_days,
        scheduled_days=py_card.scheduled_days,
        reps=py_card.reps,
        lapses=py_card.lapses,
        state=FSRSCardState(py_card.state.value),
        last_review=None
    )

def process_review(
    training_data: FSRSTrainingData,
    rating: Rating,
    review_time: datetime
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
    
    # Convert back to our training data
    return FSRSTrainingData(
        due=updated_py_card.due,
        stability=updated_py_card.stability,
        difficulty=updated_py_card.difficulty,
        elapsed_days=updated_py_card.elapsed_days,
        scheduled_days=updated_py_card.scheduled_days,
        reps=updated_py_card.reps,
        lapses=updated_py_card.lapses,
        state=FSRSCardState(updated_py_card.state.value),
        last_review=review_time
    )

def _to_py_card(training_data: FSRSTrainingData) -> PyFSRSCard:
    """Convert FSRSTrainingData to py-fsrs Card."""
    card = PyFSRSCard()
    card.due = training_data.due
    card.stability = training_data.stability
    card.difficulty = training_data.difficulty
    card.elapsed_days = training_data.elapsed_days
    card.scheduled_days = training_data.scheduled_days
    card.reps = training_data.reps
    card.lapses = training_data.lapses
    card.state = PyFSRSState(training_data.state.value)
    card.last_review = training_data.last_review
    return card
```

## Usage Examples

### Basic Usage Pattern

```python
from langtools.main.fsrs import new_training_data, process_review, Rating
from datetime import datetime, timezone

# 1. Create initial training data for a new learning item
training_data = new_training_data()
print(f"New item due: {training_data.due}")

# 2. Process first review (user forgot the item)
review_time = datetime.now(timezone.utc)
training_data = process_review(training_data, Rating.AGAIN, review_time)

print(f"After failed review:")
print(f"  - Next due: {training_data.due}")
print(f"  - Lapses: {training_data.lapses}")

# 3. Process second review (user remembered)
review_time = datetime.now(timezone.utc)
training_data = process_review(training_data, Rating.GOOD, review_time)

print(f"After successful review:")
print(f"  - Next due: {training_data.due}")
print(f"  - Interval: {training_data.scheduled_days} days")
print(f"  - State: {training_data.state}")
```

### Integration with Learning Applications

```python
# Example: Vocabulary learning app integration
from langtools.main.fsrs import new_training_data, process_review, Rating
from datetime import datetime, timezone

class VocabularyCard:
    def __init__(self, word: str, definition: str):
        self.word = word
        self.definition = definition
        self.fsrs_data = new_training_data()
    
    def review(self, rating: Rating):
        review_time = datetime.now(timezone.utc)
        self.fsrs_data = process_review(self.fsrs_data, rating, review_time)
    
    def is_due_for_review(self) -> bool:
        return self.fsrs_data.due <= datetime.now(timezone.utc)

# Usage
card = VocabularyCard("hello", "hola")
if card.is_due_for_review():
    card.review(Rating.GOOD)
    print(f"Review completed. Next due: {card.fsrs_data.due}")
```

## Configuration

The FSRS functions use a default scheduler configuration optimized for general learning:

```python
# Default configuration (built into the module)
_DEFAULT_SCHEDULER = PyFSRSScheduler(
    desired_retention=0.90,        # 90% retention rate
    learning_steps=[1, 10],        # 1 min, 10 min for new cards
    relearning_steps=[10],         # 10 min for failed cards
    enable_fuzzing=True            # Add randomness to intervals
)
```

Custom scheduler configuration will be added later when needed.

## Implementation Notes

### Dependencies

The FSRS module requires only:
- `fsrs` package (py-fsrs) for core FSRS algorithms
- Python standard library (`datetime`, `enum`)

### Thread Safety

Both functions are stateless and thread-safe. The global scheduler instance can be safely shared across multiple threads or async contexts.

### Performance Considerations

- Both operations are O(1) time complexity
- Training data objects are simple dataclasses
- No memory overhead - pure computational operations
- Suitable for high-frequency review processing

### Error Handling

Functions raise `ValueError` for:
- Invalid ratings (not 1-4)

```python
from datetime import datetime, timezone

try:
    review_time = datetime.now(timezone.utc)
    updated_data = process_review(training_data, Rating.GOOD, review_time)
except ValueError as e:
    print(f"Review processing failed: {e}")
```

## Testing Strategy

### Unit Tests

```python
import unittest
from datetime import datetime, timezone, timedelta
from langtools.main.fsrs import new_training_data, process_review, Rating, FSRSCardState

class TestFSRSFunctions(unittest.TestCase):
    
    def test_new_training_data(self):
        """Test creation of initial training data."""
        training_data = new_training_data()
        
        self.assertEqual(training_data.state, FSRSCardState.NEW)
        self.assertEqual(training_data.reps, 0)
        self.assertEqual(training_data.lapses, 0)
        self.assertIsNone(training_data.last_review)
        self.assertGreater(training_data.stability, 0)
        self.assertGreater(training_data.difficulty, 0)
    
    def test_process_review_good(self):
        """Test processing a successful review."""
        training_data = new_training_data()
        review_time = datetime.now(timezone.utc)
        
        updated_data = process_review(training_data, Rating.GOOD, review_time)
        
        self.assertEqual(updated_data.reps, 1)
        self.assertEqual(updated_data.last_review, review_time)
        self.assertGreater(updated_data.scheduled_days, training_data.scheduled_days)
    
    def test_process_review_again(self):
        """Test processing a failed review."""
        training_data = new_training_data()
        review_time = datetime.now(timezone.utc)
        
        updated_data = process_review(training_data, Rating.AGAIN, review_time)
        
        self.assertEqual(updated_data.lapses, 1)
        self.assertEqual(updated_data.last_review, review_time)
    
    def test_invalid_rating(self):
        """Test invalid rating raises ValueError."""
        training_data = new_training_data()
        review_time = datetime.now(timezone.utc)
        
        with self.assertRaises(ValueError):
            process_review(training_data, 5, review_time)  # Invalid rating
    
    def test_due_date_checking(self):
        """Test due date functionality."""
        training_data = new_training_data()
        
        # Should be due immediately for new cards
        self.assertTrue(training_data.due <= datetime.now(timezone.utc))
```

### Integration Tests

Test the functions with different review patterns to ensure proper scheduling behavior.

## Future Enhancements

1. **Custom Schedulers**: When needed, add support for different FSRS configurations
2. **Utility Functions**: Add functions like `get_retrievability()` and `is_due()` if needed
3. **Serialization**: Support for converting training data to/from JSON if needed

The design focuses on the essential FSRS operations while maintaining maximum simplicity.

