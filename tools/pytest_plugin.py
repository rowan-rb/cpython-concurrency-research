import pytest
from tools.interleave_detector import watch

@pytest.fixture
def detect_interleaves():
    """
    Pytest fixture to detect interleavings in a block of code.
    Usage:
        def test_my_counter(detect_interleaves):
            with detect_interleaves:
                # code to test
                pass
    """
    with watch() as w:
        yield w
