# tests/test_utils.py
import streamlit_analytics2.utils as utils


def test_format_seconds():
    # Test cases for format_seconds function
    assert utils.format_seconds(0) == "00:00:00", "Should format 0 seconds correctly"
    assert (
        utils.format_seconds(3661) == "01:01:01"
    ), "Should format 3661 seconds correctly"
    assert utils.format_seconds(60) == "00:01:00", "Should format 60 seconds correctly"
    assert (
        utils.format_seconds(86399) == "23:59:59"
    ), "Should handle edge cases correctly"


def test_replace_empty():
    # Test cases for replace_empty function
    assert utils.replace_empty("") == " ", "Should replace empty string with a space"
    assert utils.replace_empty(None) == " ", "Should replace None with a space"
    assert (
        utils.replace_empty("text") == "text"
    ), "Should return the original string if not empty"
