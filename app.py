from flask import Flask, render_template, request
from sign_in import sign_in_student, not_signed_in_names
from check_out import not_checked_out_names, check_out_student
from check_in import checked_out_names, check_in_student
from school_schedule import registration_open, sign_out_open, check_for_closing_email

app = Flask(__name__, static_url_path='', static_folder='static',template_folder='Templates')

# if the time is between 7:00 and 9:30 return sign-in page, if time is between 9:30 and 3:15 return campus sign-out page
def current_page():
    if registration_open():
        return render_template("sign-in.html", names=not_signed_in_names())
    elif sign_out_open():
        return render_template("sign-out.html")
    else:
        return render_template("closed.html")

# home could be sign_in
@app.route('/', methods=["GET", "POST"])
def home():
    return current_page()

@app.route('/sign_in', methods=["GET","POST"])
def sign_in():
    # If this is a form submission, attempt to register the student
    if request.method == "POST":
        student = request.form["student"]
        sign_in_student(student)
    return current_page()
    
"""
check out and check in are under the umbrella of sign out.
Because time by itself is not enough to tell whether check_out or check_in should be open
When navigated to the page checks if it CAN be open based on time.
On a post request it returns to the sign_out home screen
only one call to current_page is necessary, but I included two to make the logic more obvious
"""
@app.route('/check_out',methods=["GET","POST"])
def check_out():
    if request.method == "POST":
        student = request.form["student"]
        check_out_student(student)
        return current_page()
    elif request.method == "GET" and sign_out_open():
        check_for_closing_email()
        return render_template("check-out.html",names=not_checked_out_names())
    # on post request go back to the sign out homescreen, or if it is now closed go to the closed screen
    else:
        return current_page()
        

@app.route('/check_in',methods=["GET","POST"])
def check_in():
    if request.method == "POST":
        student = request.form["student"]
        check_in_student(student)
        return current_page()
    elif request.method == "GET" and sign_out_open():
        return render_template("check-in.html",names=checked_out_names())
        # on post request go back to the sign out homescreen, or if it is now closed go to the closed screen
    else:
        return current_page()

if __name__ == '__main__':
    app.run(debug=False, port=8000)