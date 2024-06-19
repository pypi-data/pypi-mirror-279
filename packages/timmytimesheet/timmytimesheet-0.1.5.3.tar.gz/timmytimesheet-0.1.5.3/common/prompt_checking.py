import typer

from common.TimeEntry import TimeEntry
from common.TimeSheet import TimeSheet

def validated_prompter(prompt_text, validation_fn = None):
    """
    gives the user a prompt to enter text then runs validation on it. If vlaidation_fn is
    None, it's asusmed no validation is required and (True, user_input) is returned

    Parameters:
        prompt_text (String): the prompt text for the user
        validation_fn (def function(user_input_string)): The validation function. It must return a tuple of boolean, formatted_output_string

    Returns:
        fmt_out (String): Formatted output from the validation function

    """
    try_count = 0

    while True:

        prompt_message = f"{prompt_text}"
        if try_count > 0:
            prompt_message = f"Try again... {prompt_text} ({try_count} tries)"

        user_input = typer.prompt(prompt_text)

        try:

            if not validation_fn:
                return user_input.strip()

            is_valid, fmt_out = validation_fn(user_input)
            if is_valid:
                return fmt_out
            else:
                try_count += 1

        except Exception as err:
            print(err)

def check_date_entry(input_date_string):
    time_entry_obj = TimeEntry("today", "now")
    try:
        parsed_date = time_entry_obj.parse_date_string(input_date_string)
        return True, input_date_string
    except Exception as err:
        return False, None

def check_time_entry(input_time_string):
    time_entry = TimeEntry("today", "now")
    try:
        parsed_date = time_entry.parse_time_string(input_time_string)
        return True, input_time_string
    except Exception as err:
        return False, None

def check_end_selection(_input_time_string):
    input_time_string = _input_time_string.strip()
    if input_time_string == "d":
        return True, "d"
    if input_time_string == "t":
        return True, "t"
    return False, None

def check_duration(_input_duration_string):
    time_entry_obj = TimeEntry("today", "now")
    try:
        parsed_duration = time_entry_obj.parse_duration_string(_input_duration_string)
        return True, _input_duration_string.strip()
    except Exception as err:
        return False, None
