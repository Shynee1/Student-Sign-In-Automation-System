import smtplib
import ssl
from email.message import EmailMessage
import time
from settings_handler import get_setting

# given a list of students, sends that list to a specified email address.
def send_checked_out_students(info):
    checked_out_names = [name for name in info if info[name]["checked_out"] == True]

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    sender_email = get_setting("sender-email")
    receiver_email = get_setting("receiver-emails")
    password = get_setting("password")

    content = 'Name of checked out student, Checked back in \n'
    for name in checked_out_names:
        content += name + ", " + str(info[name]["checked_in"]) + "\n"
    
    month = time.strftime("%B")
    day = str(int(time.strftime("%d")))
    dayOfWeek = time.strftime("%A")

    msg = EmailMessage()
    msg.set_content(content)
    tagLine = "Students Who Left Campus " + dayOfWeek + " " + month + " " + day
    msg['Subject'] = tagLine
    msg['From'] = sender_email
    msg['To'] = receiver_email

    print(content)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.send_message(msg, from_addr=sender_email,
                            to_addrs=receiver_email)