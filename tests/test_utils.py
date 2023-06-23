from unittest.mock import patch

import pytest

from clt import utils


@pytest.mark.parametrize("path, expected, os", [
    ("~", True, "posix"),
    ("~/home/user", True, "posix"),
    ("/home/user", True, "posix"),
    ("home/user", False, "posix"),
    ("~", True, "nt"),
    ("~\\Users\\user", True, "nt"),
    ("~/Users/user", True, "nt"),
    ("C:", True, "nt"),
    ("C:\\Users\\user", True, "nt"),
    ("C:/Users/user", True, "nt"),
    ("F:", True, "nt"),
    ("F:\\Users\\user", True, "nt"),
    ("F:/Users/user", True, "nt"),
    ("Users\\user", False, "nt"),
    ("Users/user", False, "nt"),
])
def test_is_abs_path(path, expected, os):
    """Test if a path is an absolute path."""
    with patch("os.name", os):
        assert utils.is_abs_path(path) == expected

@pytest.mark.parametrize("path, expected, os, env", [
    ("/home/user", "/home/user", "posix", None),
    ("Desktop", "/home/user/Desktop", "posix", "/home/user"),
    ("Desktop", "~/Desktop", "posix", None),
    ("C:/Users/user", "C:/Users/user", "nt", None),
    ("C:\\Users\\user", "C:/Users/user", "nt", None),
    ("Desktop", "C:/Users/user/Desktop", "nt", "C:\\Users\\user"),
    ("Desktop\\New Folder", "~/Desktop/New Folder", "nt", None),
])
def test_normalize_path(path, expected, os, env):
    """Test if a path is normalized correctly."""
    with (patch("os.name", os),
          patch("os.getenv", return_value=env)):
        assert utils.normalize_path(path) == expected