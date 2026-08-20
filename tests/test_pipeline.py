import os
import pytest

def test_environment_setup():
    """Verify core imports and structure."""
    import duckdb
    import pandas as pd
    assert duckdb is not None
    assert pd is not None

def test_data_directory_exists():
    """Verify project directory layout."""
    assert os.path.exists("src/app.py")