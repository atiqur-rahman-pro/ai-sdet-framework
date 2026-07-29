import pytest
from utils.date_helpers import get_iso_timestamp, format_audit_duration

def test_iso_timestamp_format():
    """Verify ISO timestamp utility output."""
    timestamp = get_iso_timestamp()
    assert isinstance(timestamp, str)
    assert "T" in timestamp

def test_format_audit_duration():
    """Verify audit duration formatting helper."""
    formatted = format_audit_duration(1.4567)
    assert formatted == "1.46s"
