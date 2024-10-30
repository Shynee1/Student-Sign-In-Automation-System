import smtplib
import ssl
from email.message import EmailMessage
import time
from school_schedule import free_period
from settings_handler import get_setting

def send_reminder_students(info):
    unregistered_names = [name for name in info if info[name]["signed_in"] == False]
    #sendStudents(info, unregistered_names, True)
    print(unregistered_names)


# given a list of students, sends that list to a specified email address.
def send_not_signed_in_students(info):
    unregistered_names = [name for name in info if info[name]["signed_in"] == False]
    sendAll(info,unregistered_names)
    #sendGrades(info,unregistered_names)
    #sendStudents(info,unregistered_names, False)

def sendAll(students,unregisteredNames):

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = get_setting("sender-email")
    receiver_email = get_setting("receiver-emails")
    password = get_setting("password")

    content = 'Name, Grade \n'
    for name in unregisteredNames:
        content += name + ", " + students[name]["grade"] + '\n'
        
    freePeriod = free_period()
    month = time.strftime("%B")
    day = str(int(time.strftime("%d")))
    dayOfWeek = time.strftime("%A")

    msg = EmailMessage()
    msg.set_content(content)
    tagLine = "Students Who Didn't Sign In " + dayOfWeek + " " + month + " " + day + " " + freePeriod + " Period"
    msg['Subject'] = tagLine
    msg['From'] = sender_email
    msg['To'] = receiver_email

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg, from_addr=sender_email,
                            to_addrs=receiver_email)
        

def sendGrades(students,unregisteredNames):
    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = get_setting("sender-email")
    form_deans = get_setting("form-dean-emails")
    form_numerals = get_setting("form-numerals")
    password = get_setting("password")

    freePeriod = free_period()
    month = time.strftime("%B")
    day = str(int(time.strftime("%d")))
    dayOfWeek = time.strftime("%A")

    # send emails to form deans
    for i in range(4):
        target = form_numerals[i]
        receiver_email = form_deans[i]

        content = 'Missing Students from Form ' + target + '\n'
        missing_students = [name for name in unregisteredNames if students[name]["grade"] == target]

        if len(missing_students) == 0:
            continue

        for name in missing_students:
            content += name + '\n'

        msg = EmailMessage()
        msg.set_content(content)
        tagLine = "Students Who Didn't Sign In " + dayOfWeek + " " + month + " " + day + " " + freePeriod + " Period"
        msg['Subject'] = tagLine
        msg['From'] = sender_email
        msg['To'] = receiver_email

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.send_message(msg, from_addr=sender_email,
                                to_addrs=receiver_email)
        
    
def sendStudents(students,unregisteredNames, isReminder):
    recipients = []
    recipients.append(get_setting("receiver-emails")[0])
    
    for name in unregisteredNames:
        recipients.append(students[name]["email"])

    print(f"sending emails to :{recipients}")

    freePeriod = free_period()
    month = time.strftime("%B")
    day = str(int(time.strftime("%d")))
    dayOfWeek = time.strftime("%A")

    if (isReminder):
        content = "You haven't signed in today. You have 15 minutes to sign in on the iPad at the front desk."
        tagLine = "Reminder to sign in - " + dayOfWeek + " " + month + " " + day + " " + freePeriod + " Period"
    else:
        content = "You didn't sign in today. When you have free first period please sign in on the iPad at the front desk"
        tagLine = "You didn't sign in  - " + dayOfWeek + " " + month + " " + day + " " + freePeriod + " Period"

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = get_setting("sender-email")
    password = get_setting("password")
    
    msg = EmailMessage()
    msg.set_content(content)
    
    msg['Subject'] = tagLine
    msg['From'] = sender_email
    msg["Bcc"] = recipients

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg, from_addr=sender_email,
                            to_addrs=recipients,)