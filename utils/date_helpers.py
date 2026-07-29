from datetime import datetime, timezone

def get_iso_timestamp() -> str:
    """Generate ISO 8601 UTC timestamp string for QA audit reports."""
    return datetime.now(timezone.utc).isoformat()

def format_audit_duration(seconds: float) -> str:
    """Format execution duration into readable string format."""
    return f"{seconds:.2f}s"
