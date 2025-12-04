from datetime import timedelta
from time_utils.time_utils import _convert_to_timedelta
import pytest

class TestStrictParsing:
    def test_garbage_prefix_rejected(self):
        # These should return None, but currently might return a timedelta
        assert _convert_to_timedelta("d+30m") is None
        assert _convert_to_timedelta("1+30m") is None
        assert _convert_to_timedelta("x+1h") is None
        assert _convert_to_timedelta("invalid+30m") is None

    def test_leading_whitespace_accepted(self):
        # These should still work
        assert _convert_to_timedelta(" +30m") == timedelta(minutes=30)
        assert _convert_to_timedelta("  +1h") == timedelta(hours=1)

    def test_trailing_whitespace_accepted(self):
        assert _convert_to_timedelta("+30m ") == timedelta(minutes=30)
        assert _convert_to_timedelta("+1h  ") == timedelta(hours=1)
