"""Test helper functions."""

def strip_color_codes(s: str) -> str:
    """Remove ANSI color codes from string.
    
    Args:
        s: String containing ANSI color codes
        
    Returns:
        String with color codes removed
    """
    while "\x1b[" in s:
        start = s.find("\x1b[")
        end = s.find("m", start) + 1
        s = s[:start] + s[end:]
    return s
