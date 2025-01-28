"""Tools for working with the school schedule.
This module handles the internal representation of the school schedule,
handling vacations, registration times and the current free period.
"""
from pytz import timezone
from datetime import time, datetime
import numpy as np
from send_sign_out import send_checked_out_students
from settings_handler import get_setting, get_setting_as_date
from pathlib import Path
import json

DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"

# All times are localized and interpreted in this timezone.
TIMEZONE = timezone("America/New_York")

# Print a warning for dates outside this range:
SCHOOL_START = get_setting_as_date("school-year-start", DATE_FORMAT, TIMEZONE)
SCHOOL_END = get_setting_as_date("school-year-end", DATE_FORMAT, TIMEZONE)
# Holidays and schedule information
#   FREE_PATTERN[0] should correspond to FIRST_DAY
#   holiday format: "YYYY-MM-DD"
FREE_PATTERN = get_setting("free-pattern")
HOLIDAYS = get_setting("holidays")

# Registration opening/closing times
REGISTRATION_OPEN_TIME = get_setting_as_date("registration-open", TIME_FORMAT, TIMEZONE).time()
REGISTRATION_CLOSE_TIME = get_setting_as_date("registration-close", TIME_FORMAT, TIMEZONE).time()
REGISTRATION_WEDNESDAY_CLOSE_TIME = get_setting_as_date("registration-close-wednesday", TIME_FORMAT, TIMEZONE).time()
SCHOOL_CLOSE_TIME = get_setting_as_date("school-close", TIME_FORMAT, TIMEZONE).time()

LOGS_PATH = Path(__file__).parent.absolute() / get_setting("logs-directory-path")
        
def registration_open():
    # Check whether registration is open at a given datetime.
    timestamp=datetime.now(TIMEZONE)
    print(f"Checking registration at {timestamp}.")
    _validate_datetime(timestamp)

    # check if it is a school day
    if not _open_day(timestamp):
        print("Today is not a school day")
        return False

    # Wednesday :|
    if timestamp.strftime("%A") == "Wednesday":
        return (REGISTRATION_OPEN_TIME <= timestamp.time()) and (timestamp.time() <= REGISTRATION_WEDNESDAY_CLOSE_TIME)
    
    # Otherwise
    return (REGISTRATION_OPEN_TIME <= timestamp.time()) and (timestamp.time() <= REGISTRATION_CLOSE_TIME)

def sign_out_open():
    timestamp=datetime.now(TIMEZONE)
    _validate_datetime(timestamp)

    # check if it is a school day
    if not _open_day(timestamp):
        return False

    # Wednesday :|
    if timestamp.strftime("%A") == "Wednesday":
        return (REGISTRATION_WEDNESDAY_CLOSE_TIME <= timestamp.time()) and (timestamp.time() <= SCHOOL_CLOSE_TIME)
    
    # Otherwise
    return (REGISTRATION_CLOSE_TIME <= timestamp.time()) and (timestamp.time() <= SCHOOL_CLOSE_TIME)



def free_period():
    # Determine the element of FREE_PATTERN corresponding to the given day.
    timestamp=datetime.now()
    print(f"Checking free period for {timestamp}.")

    # Free periods rotate according to FREE_PATTERN, but only on school days
    school_days = np.busday_count(SCHOOL_START.strftime(
        "%Y-%m-%d"), timestamp.strftime("%Y-%m-%d"), holidays=HOLIDAYS)
    
    free_period = FREE_PATTERN[school_days % 7]

    print(f'Free Period: {free_period}')
    return "A"


def _validate_datetime(timestamp):
    # Print a warning if the datetime is outside of the expected range.
    if timestamp < SCHOOL_START or timestamp > SCHOOL_END:
        print(f"WARNING The given datetime '{timestamp}' is outside the valid"
              f" range ({SCHOOL_START} to {SCHOOL_END}), this may lead to unexpected behaviour.")


def _open_day(timestamp):
    # Check whether a given date is a holiday
    _validate_datetime(timestamp)
    return np.is_busday(timestamp.strftime("%Y-%m-%d"), holidays=HOLIDAYS)