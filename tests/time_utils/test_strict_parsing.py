from datetime import timedelta
from time_utils.time_utils import _convert_to_timedelta
import pytest

class TestStrictParsing:
    def test_garbage_prefix_rejected(self):
        # These should return None
        assert _convert_to_timedelta("d+30m") is None
        assert _convert_to_timedelta("1+30m") is None
        assert _convert_to_timedelta("x+1h") is None
        assert _convert_to_timedelta("invalid+30m") is None

    def test_leading_whitespace_rejected(self):
        # User requested strict parsing where "   +30m" returns None
        assert _convert_to_timedelta(" +30m") is None
        assert _convert_to_timedelta("  +1h") is None

    def test_trailing_whitespace_rejected(self):
        # User requested strict parsing where "+30m " returns None
        assert _convert_to_timedelta("+30m ") is None
        assert _convert_to_timedelta("+1h  ") is None
        assert _convert_to_timedelta("+1h garbage") is None
