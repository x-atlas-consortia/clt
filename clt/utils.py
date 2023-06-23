import os
import re


def is_abs_path(path: str) -> bool:
    """Check if a path is an absolute path."""
    if path.startswith("~"):
        return True

    if os.name == "nt":
        # Windows
        return re.match(r"^(?:[a-zA-Z]):", path) is not None
    else:
        # The rest
        return path.startswith("/")

def normalize_path(path: str) -> str:
    """Normalize a path to an absolute path using slashes ('/'). If the path is
       relative, it will be prefixed with the user's home directory ('~')."""
    if is_abs_path(path) is False:
        if os.name == "nt" and os.getenv("USERPROFILE") is not None:
            # Windows
            path = os.path.join(os.getenv("USERPROFILE"), path)
        elif os.getenv("HOME") is not None:
            # Posix and potentially Windows
            path = os.path.join(os.getenv("HOME"), path)
        else: 
            # Fallback
            path = os.path.join("~", path)

    return path.replace("\\", "/")