import os
import json
import csv
from school_schedule import free_period, TIMEZONE, DATE_FORMAT
from settings_handler import get_setting, get_setting_as_date
from time_manager import start_email_thread
from datetime import timezone
from pathlib import Path

LOG_FORMAT = "%Y-%m-%d.json"
NAME_INDEX = 0
GRADE_INDEX = 1
PERIOD_INDEX = 2
EMAIL_INDEX = 3

def _filename(date):
    """Construct a filename corresponding to a given date. Returns "logs/YYYY-MM-DD.json" """
    return Path(__file__).parent.absolute() / get_setting("logs-directory-path") / date.strftime(LOG_FORMAT)


def _write_student_file(students, date):
    """Write student information to "logs/YYYY-MM-DD.json", overwriting any existing contents."""
    with open(_filename(date), "w+") as file:
        json.dump(students, file)

def _read_or_initialize_student_file(date):
    """Open a student file for reading, initializing a new file if necessary.

    Looks for student data in "logs/YYYY-MM-DD.json".
    New files will be initialized from the school school schedule.
    """
    if not os.path.exists(_filename(date)):
        print("creating daily file")
        students = get_students(free_period(), date)
        _write_student_file(students, date)
        start_email_thread()

    with open(_filename(date), "r") as file:
        return json.load(file)

# Returns the list of students who have the given free period first
def get_students(period, date):
    students = {}

    # CSV data as a multi-line string
    # should include all fifth (and for most of the year sixth) formers
    csv_filepath = Path(__file__).parent.absolute() / get_setting("data-directory-path") / get_setting("student-data-file")
    csv_data = open(csv_filepath, "r")

    # creating a csv reader object from the multi-line string
    csvreader = csv.reader(csv_data)

    # extracting field names through first row,
    fields = next(csvreader)

    senior_leave_date = get_setting_as_date("senior-leave-date", DATE_FORMAT, TIMEZONE)

    # extracting each data row one by one
    for row in csvreader:
        free = row[PERIOD_INDEX]
        grade = row[GRADE_INDEX]
        name = row[NAME_INDEX]
        email = row[EMAIL_INDEX]

        if name in students:
            signed_in = students[name]["signed_in"]
        else:   
            signed_in = True

        if free == period:
            signed_in = False

        if grade == "IV" or grade == "V" or (grade == "VI" and date < senior_leave_date):
            students[name] = {"signed_in": signed_in, "checked_out": False, "checked_in": False, "grade": grade, "email": email}

    for student in students:
        if students[student]["signed_in"] == False:
            print(student)

    csv_data.close()

    return students