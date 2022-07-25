import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ngo.db")

@app.route("/")
@login_required
def index():
    """Show user´s active courses"""

    #Query for courses data in course table
    mycourses = db.execute("SELECT course FROM courses WHERE people =?", session["user_id"])

    #render page
    return render_template("index.html", mycourses_t=mycourses)

@app.route("/signup", methods=["POST"])
@login_required
def signup():
    """Sign up to courses"""

    #Get selected course
    sel_course = request.form.get("courses")

    #Check against server side data when signing in
    available = db.execute("SELECT course FROM courses_all")
    allcourses = []
    for i in available:
        allcourses.append(i["course"])

    #Check if selected course is actually in available courses
    if request.form.get("courses") not in allcourses:
        return apology("Not an available course")

    #Check if at least one course was selected
    if not request.form.get("courses"):
        return apology("Please select a course")

    #Check if already signed in for that course
    checklist = db.execute("SELECT people FROM courses WHERE course = ?", sel_course)
    for i in checklist:
        if session["user_id"] == i["people"]:
            return apology("already in this course")

    #Sign user up writing in table
    db.execute("INSERT INTO courses (course, people) VALUES (?, ?)", sel_course, session["user_id"])

    return redirect("/")

@app.route("/allcourses")
@login_required
def all_available():
    """Show list of all available courses"""

    #Query for all available courses in table courses, with corresponding day & time
    allc = db.execute("SELECT course, day, time FROM courses_all")

    return render_template("allcourses.html", allc=allc)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM students WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Please check username and/or password or register first", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/contact")
@login_required
def contact():
    """Show contact info"""

    #render page
    return render_template("contact.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/findcourse")
@login_required
def findcourse():
    """Displays available courses"""

    #Query courses from database
    allcourses = db.execute("SELECT course FROM courses_all")

    return render_template("findcourse.html", courses = allcourses)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        #Access form data:
        username = request.form.get("username")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")

        # Ensure username does not already exist
        userslist = db.execute("SELECT username FROM students")
        for i in userslist:
            if username == i["username"]:
                return apology("username already exists")

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password")

        #Check that the user typed in password correctly:
        elif password != confirm:
            return apology("password and confirmation do not match")
            return render_template("register.html")

        #Hash user´s password
        else:
            hash = generate_password_hash(password)

            #insert data into tables
            db.execute("INSERT INTO students (username, hash) VALUES (?, ?)", username, hash)

            # Redirect user to login form
            return redirect("/")

    elif request.method == "GET":

        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
