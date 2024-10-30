import json
from threading import Thread
from datetime import datetime, timedelta
from datetime import date as date_function
from send_sign_in import send_not_signed_in_students, send_reminder_students
from settings_handler import get_setting
from send_sign_out import send_checked_out_students
from school_schedule import _open_day, TIMEZONE, REGISTRATION_CLOSE_TIME, REGISTRATION_WEDNESDAY_CLOSE_TIME, SCHOOL_CLOSE_TIME
from pathlib import Path

# Starts separate thread to monitor times and automate email sending
# Starts when log file is created for each day
# Ends at the end of the school day
def start_email_thread():
    email_thread = Thread(target=email_scheduler)
    email_thread.start()

# Runs every "frame" and checks whether it should be sending an email
def email_scheduler():
    date = datetime.now(TIMEZONE)
    day_of_week = date.strftime("%A")
    time = date.time()

    print(f"Email scheduling task started at {time} on {day_of_week}")

    if (not _open_day(date)):
       print(f"Not a valid school day, canceling task")
       return

    if day_of_week == "Wednesday":
        registration_end_time = REGISTRATION_WEDNESDAY_CLOSE_TIME
    else:
        registration_end_time = REGISTRATION_CLOSE_TIME

    # Subtract reminder email offset from registration time
    reminder_email_offset = int(get_setting("reminder-email-offset"))
    registration_reminder_time = (
        datetime.combine(date_function(1, 1, 1), registration_end_time) - 
        timedelta(minutes = reminder_email_offset)
    ).time()

    reminder_email_sent = False
    signin_email_sent = False

    # Loop for the entire school day 
    while time <= SCHOOL_CLOSE_TIME:
        date = datetime.now(TIMEZONE)
        time = date.time()
        
        # Check if should be sending a reminder email
        if times_equal(time, registration_reminder_time) and not reminder_email_sent:
            send_reminder_email()
            reminder_email_sent = True

        # Check if should be sending the sign-in email
        if times_equal(time, registration_end_time) and not signin_email_sent:
            send_not_signed_in_email()
            signin_email_sent = True
    
    # Send email of students who checked in/out
    send_closing_email()

def send_reminder_email():
    filename = get_log_filename()
    with open(filename, "r") as file:
        data = json.loads(file.read())
        send_reminder_students(data)
    print("Reminder email sent")

def send_not_signed_in_email():
    filename = get_log_filename()
    with open(filename, "r") as file:
        data = json.loads(file.read())
        send_not_signed_in_students(data)
    print("Sign In Email Sent")

def send_closing_email():
    filename = get_log_filename()
    with open(filename, "r") as file:
        data = json.loads(file.read())
        send_checked_out_students(data)
    print("Closing email sent")

def get_log_filename():
    return Path(__file__).parent.absolute() / get_setting("logs-directory-path") / datetime.now().strftime("%Y-%m-%d.json")

def times_equal(timeA, timeB):
    return (timeA.hour == timeB.hour) and (timeA.minute == timeB.minute)