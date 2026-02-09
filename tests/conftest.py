"""Pytest configuration for tests."""

import sys
from pathlib import Path

# Add the project root to sys.path so that imports work correctly
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
