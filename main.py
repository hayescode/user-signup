from flask import Flask, request, redirect, render_template
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/")
def index():
    return render_template("form.html",username="",email="",username_error="",password_error="",verify_password_error="",email_error="")

def is_empty(string):    #to test if username/password/verify_password is empty
    if string == "":
        return True
    else:
        return False

@app.route("/", methods=["POST"])
def validate_submission():    #throws errors is conditions are not met
    username = request.form["username"]
    password = request.form["password"]
    verify_password = request.form["verify_password"]
    email = request.form["email"]

    username_error = ""
    password_error = ""
    verify_password_error = ""
    email_error = ""

    #check if username/password/verify_password is empty
    if is_empty(username):
        username_error = "Must type username"
    if is_empty(password):
        password_error = "Must type password"
    if is_empty(verify_password):
        verify_password_error = "Must re-type password"

    #check username/password for any spaces and length between 3 and 20 characters
    for i in username:
        if i == " ":
            username_error = "Cannot contain space characters"
    if len(username) < 3 or len(username) > 20:    #checks that the length of the submission is between 3 and 20 characters
        username_error = "Must be between 3 and 20 characters"

    for i in password:
        if i == " ":
            password_error = "Cannot contain space characters"
    if len(password) < 3 or len(password) > 20:    #checks that the length of the submission is between 3 and 20 characters
        password_error = "Must be between 3 and 20 characters"

    #checks if password and verify_password match
    if password != verify_password:
        verify_password_error = "Passwords do not match"

    #checks email for > 1 @ or . symbol and length between 3 and 20
    space_count = 0
    at_symbol_count = 0
    period_symbol_count = 0
    for i in email:
        if i == " ":
            space_count += 1
        if i == "@":
            at_symbol_count += 1
        if i == ".":
            period_symbol_count += 1
    if space_count > 0:
        email_error = "Cannot contain spaces"
    elif at_symbol_count > 1:
        email_error = "Cannot contain more than one '@' symbol"
    elif period_symbol_count > 1:
        email_error = "Cannot contain more than on '.' symbol"
    elif len(email) < 3 or len(email) > 20:
        email_error = "Must be between 3 and 20 characters"

    #either redirect to welcome page or display errors
    if username_error == "" and password_error == "" and verify_password_error == "" and email_error == "":
        return redirect("/welcome?u={0}".format(username))
    else:
        return render_template("form.html",username=username,email=email,username_error=username_error,password_error=password_error,verify_password_error=verify_password_error,email_error=email_error)
    
@app.route('/welcome')
def welcome():
    u = request.args.get('u')
    return render_template("welcome.html", username=u)
app.run()