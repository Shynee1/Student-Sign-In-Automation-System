"""
Uses the same tools as 'sign_in.py'
"""

from datetime import datetime
from custom_logging import _read_or_initialize_student_file
from custom_logging import _filename
from custom_logging import _write_student_file
from school_schedule import TIMEZONE

def checked_out_names(grades=["V", "VI"]):
    date = datetime.now(TIMEZONE)
    students = _read_or_initialize_student_file(date)
    return [name for name, info in students.items() if info["grade"] in grades and info["checked_out"] and not info["checked_in"]]


def check_in_student(name):
    date = datetime.now(TIMEZONE)
    students = _read_or_initialize_student_file(date)
    if name not in students:
        print(f"WARNING: Student '{name}' not found in {_filename(date)}.")

    if students[name]["checked_in"]:
        print(f"WARNING Student {name} is already checked in in {_filename(date)}.")
    if not students[name]["checked_out"]:
        print(f"Checked out: {name}")
        
    students[name]["checked_in"] = True
    _write_student_file(students, date)




