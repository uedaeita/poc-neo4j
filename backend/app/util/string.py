from typing import Optional


def clean_str(s: Optional[str]) -> Optional[str]:
    if not s:
        return None
    return s.replace("\n", "").replace("\r", "").replace("\\", "").replace('"', "")
