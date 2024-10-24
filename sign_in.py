"""Tools for working with the list of current students.
This module provides functions for working with a list of students
and storing the results to disk.
"""

from datetime import datetime
from custom_logging import _read_or_initialize_student_file
from custom_logging import _filename
from custom_logging import _write_student_file
from custom_logging import TIMEZONE

def not_signed_in_names():
    date = datetime.now(TIMEZONE)
    """Return the names of unregistered students matching `grades` for a given date.
    Looks for student data in "logs/YYYY-MM-DD.json". If necessary, a new file will be created
    with students populated from the school schedule.
    """
    # Look for the file, if it doesn't exist create it and populate it.
    students = _read_or_initialize_student_file(date)
    return [name for name, info in students.items() if not info["signed_in"]]


def sign_in_student(name):
    date = datetime.now(TIMEZONE)
    """Mark a student as registered for a given date.
    Looks for student data in "logs/YYYY-MM-DD.json". If necessary, a new file will be created
    with students populated from the school schedule.
    """
    students = _read_or_initialize_student_file(date)
    if name not in students:
        print(f"WARNING: Student '{name}' not found in {_filename(date)}.")

    if students[name]["signed_in"]:
        print(f"WARNING Student {name} is already registered in {_filename(date)}.")
    if not students[name]["signed_in"]:
        print(f"Signed in: {name}")
        
    students[name]["signed_in"] = True
    _write_student_file(students, date)




