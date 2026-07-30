import pytest
from utils.websocket_helpers import is_valid_ws_url, parse_ws_frame_size

def test_is_valid_ws_url():
    """Verify WebSocket URL scheme validator."""
    assert is_valid_ws_url("wss://echo.websocket.org") is True
    assert is_valid_ws_url("ws://localhost:8080") is True
    assert is_valid_ws_url("https://example.com") is False

def test_parse_ws_frame_size():
    """Verify WebSocket payload byte size calculator."""
    size = parse_ws_frame_size("hello world")
    assert size == 11
    assert parse_ws_frame_size("") == 0
