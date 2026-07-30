from typing import Any, Dict

def is_valid_ws_url(url: str) -> bool:
    """Validate if given URL string uses WebSocket scheme (ws:// or wss://)."""
    return url.startswith("ws://") or url.startswith("wss://")

def parse_ws_frame_size(payload: str) -> int:
    """Calculate byte size of a WebSocket frame payload string."""
    return len(payload.encode("utf-8")) if payload else 0
