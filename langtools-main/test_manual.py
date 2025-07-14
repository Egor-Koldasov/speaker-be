#!/usr/bin/env python3
"""Manual test to verify FSRS implementation structure."""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that our modules can be imported."""
    try:
        from langtools.main.fsrs.models import FSRSTrainingData, FSRSCardState, Rating
        print("✓ Successfully imported models")
        
        # Test enum values
        assert Rating.AGAIN == 1
        assert Rating.HARD == 2  
        assert Rating.GOOD == 3
        assert Rating.EASY == 4
        print("✓ Rating enum values correct")
        
        assert FSRSCardState.NEW == 0
        assert FSRSCardState.LEARNING == 1
        assert FSRSCardState.REVIEW == 2
        assert FSRSCardState.RELEARNING == 3
        print("✓ FSRSCardState enum values correct")
        
        # Test dataclass creation
        from datetime import datetime, timezone
        now = datetime.now(timezone.utc)
        
        training_data = FSRSTrainingData(
            due=now,
            stability=2.0,
            difficulty=5.0,
            elapsed_days=0,
            scheduled_days=1,
            reps=0,
            lapses=0,
            state=FSRSCardState.NEW
        )
        print("✓ FSRSTrainingData dataclass works")
        
        # Test mutability
        training_data.reps = 1
        assert training_data.reps == 1
        print("✓ FSRSTrainingData is mutable")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_structure():
    """Test file structure."""
    expected_files = [
        'src/langtools/__init__.py',
        'src/langtools/main/__init__.py', 
        'src/langtools/main/fsrs/__init__.py',
        'src/langtools/main/fsrs/models.py',
        'src/langtools/main/fsrs/functions.py',
        'tests/fsrs/__init__.py',
        'tests/fsrs/test_models.py',
        'tests/fsrs/test_functions.py',
        'pyproject.toml',
        'README.md'
    ]
    
    missing = []
    for file_path in expected_files:
        if not os.path.exists(file_path):
            missing.append(file_path)
    
    if missing:
        print(f"❌ Missing files: {missing}")
        return False
    else:
        print("✓ All expected files present")
        return True

if __name__ == "__main__":
    print("Testing FSRS implementation structure...")
    
    structure_ok = test_structure()
    imports_ok = test_imports()
    
    if structure_ok and imports_ok:
        print("\n🎉 All structural tests passed!")
        print("\nNote: To test full functionality, install 'fsrs' package:")
        print("pip install fsrs")
    else:
        print("\n❌ Some tests failed")
        sys.exit(1)