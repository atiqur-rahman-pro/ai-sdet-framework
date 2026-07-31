from typing import Optional

def format_frame_title(frame_name: Optional[str]) -> str:
    """Format frame identifier name for logging in QA reports."""
    return f"Frame[{frame_name}]" if frame_name else "Frame[main_context]"

def is_shadow_host_selector(selector: str) -> bool:
    """Check if CSS selector targets shadow host element."""
    return "shadow" in selector.lower() or "root" in selector.lower()
