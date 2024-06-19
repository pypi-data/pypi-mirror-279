import pytest

from common.prompt_checking import validated_prompter
from common.prompt_checking import check_date_entry, check_time_entry
from common.prompt_checking import check_end_selection
from common.prompt_checking import check_duration

@pytest.mark.parametrize("input_string, expected_is_valid", [
    ("fdsafdsa", False),
    ("tdy", False),
    ("today", True),
    ("1/5/2024", True),
])
def test_check_date_entry_validity_check(input_string, expected_is_valid):
    is_valid, fmt_out = check_date_entry(input_string)
    assert is_valid == expected_is_valid, f"{input_string} should have resolved {expected_is_valid}"

@pytest.mark.parametrize("input_string, expected_fmt_out", [
    ("fdsafdsa", None),
    ("tdy", None),
    ("today", "today"),
    ("1/5/2024", "1/5/2024"),
])
def test_check_date_entry_formatted_output(input_string, expected_fmt_out):
    is_valid, fmt_out = check_date_entry(input_string)
    assert fmt_out == expected_fmt_out, f"{input_string} should have resolved {expected_fmt_out}"

@pytest.mark.parametrize("input_string, expected_is_valid", [
    ("fdsafdsa", False),
    ("tdy", False),
    ("now", True),
    ("3pm", True),
])
def test_check_time_entry_validity_check(input_string, expected_is_valid):
    is_valid, fmt_out = check_time_entry(input_string)
    assert is_valid == expected_is_valid, f"{input_string} should have resolved {expected_is_valid}"

@pytest.mark.parametrize("input_string, expected_fmt_out", [
    ("fdsafdsa", None),
    ("tdy", None),
    ("now", "now"),
    ("1pm", "1pm"),
])
def test_check_time_entry_formatted_output(input_string, expected_fmt_out):
    is_valid, fmt_out = check_time_entry(input_string)
    assert fmt_out == expected_fmt_out, f"{input_string} should have resolved {expected_fmt_out}"

@pytest.mark.parametrize("input_string, expected_is_valid", [
    ("d", True),
    ("t", True),
    ("d ", True),
    ("t \r\n", True),
    ("tfdas", False),
])
def test_check_end_selection_validity_check(input_string, expected_is_valid):
    is_valid, fmt_out = check_end_selection(input_string)
    assert is_valid == expected_is_valid, f"{input_string} should have resolved {expected_is_valid}"

@pytest.mark.parametrize("input_string, expected_fmt_out", [
    ("d", "d"),
    ("t", "t"),
    ("d ", "d"),
    ("t \r\n", "t"),
    ("tfdas", None),
])
def test_check_end_selection_formatted_output(input_string, expected_fmt_out):
    is_valid, fmt_out = check_end_selection(input_string)
    assert fmt_out == expected_fmt_out, f"{input_string} should have been formatted as '{expected_fmt_out}'"

@pytest.mark.parametrize("input_string, expected_is_valid", [
    ("3", False),
    ("abc", False),
    ("3hrs", True),
    ("5min", True),
])
def test_check_duration_validity_check(input_string, expected_is_valid):
    is_valid, fmt_out = check_duration(input_string)
    assert is_valid == expected_is_valid, f"{input_string} should have resolved {expected_is_valid}"

@pytest.mark.parametrize("input_string, expected_fmt_out", [
    ("3", None),
    ("abc", None),
    ("3hrs", "3hrs"),
    ("5min", "5min"),
])
def test_check_duration_formatted_output(input_string, expected_fmt_out):
    is_valid, fmt_out = check_duration(input_string)
    assert fmt_out == expected_fmt_out, f"{input_string} should have been formatted as '{expected_fmt_out}'"
