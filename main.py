from flask import Flask, request, redirect
import cgi

app = Flask(__name__)
app.config['DEBUG'] = True

form = """
<!doctype html>
<html>
    <title>User Signup</title>
    <body>
        <form action="/welcome" method="POST">
            <h1>Signup</h1>
            <label for="username">Username</label>
                <input type="text" name="username" value="{username}"/>
                <span>{username_error}</span>
                <br>
            <label for="password">Password</label>
                <input type="password" name="password" />
                <span>{password_error}</span>
                <br>
            <label for="verify_password">Verify Password</label>
                <input type="password" name="verify_password" />
                <span>{verify_password_error}</span>
                <br>
            <label for="email">Email (optional)</label>
                <input type="text" name="email" value="{email}" />
                <span>{email_error}</span>
                <br>
            <input type="submit" />
        </form>
    </body>
</html>
"""

@app.route("/")
def index():
    return form

def is_empty(string):    #to test if username/password/verify_password is empty
    if string == "":
        return True
    else:
        return False

def valid_parameters(string):    #checks if there is a space in the submission
    for i in string:
        if i == " ":
            return "Cannot contain space characters"
    if len(string) < 3 or len(string) > 20:    #checks that the length of the submission is between 3 and 20 characters
        return "Must be between 3 and 20 characters"
    else:
        return True

def validate_email(string):    #checks email for spaces, number of @ and . characters, and length between 3 and 20
    space_count = 0
    at_symbol_count = 0
    period_symbol_count = 0
    for i in string:
        if i == " ":
            space_count += 1
        if i == "@":
            at_symbol_count += 1
        if i == ".":
            period_symbol_count += 1
    if space_count > 0:
        return "Cannot contain spaces"
    elif at_symbol_count > 1:
        return "Cannot contain more than one '@' symbol"
    elif period_symbol_count > 1:
        return "Cannot contain more than on '.' symbol"
    elif len(string) < 3 or len(string) > 20:
        return "Must be between 3 and 20 characters"
    else:
        return True

@app.route("/", methods=["POST"])
def validate_submission():
    username = request.form("username")
    password = request.form("password")
    verify_password = request.form("verify_password")
    email = request.form("email")

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
    if not valid_parameters(username):
        username_error = valid_parameters(username)
    if not valid_parameters(password):
        password_error = valid_parameters(password)

    #checks if password and verify_password match
    if password != verify_password:
        verify_password_error = "Passwords do no match"

    


app.run()