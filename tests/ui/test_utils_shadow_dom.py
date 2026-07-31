import pytest
from utils.shadow_dom_helpers import format_frame_title, is_shadow_host_selector

def test_format_frame_title():
    """Verify frame title formatting helper."""
    assert format_frame_title("login_iframe") == "Frame[login_iframe]"
    assert format_frame_title(None) == "Frame[main_context]"

def test_is_shadow_host_selector():
    """Verify shadow host selector validator."""
    assert is_shadow_host_selector("#shadow-root-host") is True
    assert is_shadow_host_selector("div.container") is False
