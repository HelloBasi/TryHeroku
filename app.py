from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, user_login_required, collector_login_required

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
db = SQL("sqlite:///Recycle.db")

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/profile")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route('/logout')
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        if not (email := request.form.get("email")):
            return apology("MISSING USERNAME")

        if not (password := request.form.get("password")):
            return apology("MISSING PASSWORD")

        if not (confirmation := request.form.get("confirmation")):
            return apology("PASSWORD DON'T MATCH")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE email = ?;", email)

        # Ensure username not in database
        if len(rows) != 0:
            return apology(f"The user '{email}' already exists. Please choose another email.")

        # Ensure first password and second password are matched
        if password != confirmation:
            return apology("password not matched")

        # Insert all into database
        id = db.execute("INSERT INTO users (email, hash, name, phone_number) VALUES (?, ?, ?, ?);",
                        email, generate_password_hash(password), request.form.get("name"), request.form.get("phone_number"))

        # Remember which user has logged in
        session["user_id"] = id

        flash("Registered!")

        return redirect("/profile")
    else:
        return render_template("register.html")


@app.route("/collector/login", methods=["GET", "POST"])
def collector_login():
    """Log collector in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email"):
            return apology("must provide email", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM collectors WHERE email = :email",
                          email=request.form.get("email"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["collector_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/collector/profile")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("collector_login.html")
    

@app.route("/collector/logout")
def collector_logout():
    """Log collector out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/collector/register", methods=["GET", "POST"])
def collector_register():
    """Register collector"""
    if request.method == "POST":

        if not (email := request.form.get("email")):
            return apology("MISSING USERNAME")

        if not (password := request.form.get("password")):
            return apology("MISSING PASSWORD")

        if not (confirmation := request.form.get("confirmation")):
            return apology("PASSWORD DON'T MATCH")

        # Query database for username
        rows = db.execute("SELECT * FROM collectors WHERE email = ?;", email)

        # Ensure username not in database
        if len(rows) != 0:
            return apology(f"The user '{email}' already exists. Please choose another email.")

        # Ensure first password and second password are matched
        if password != confirmation:
            return apology("password not matched")

        # Insert all into database
        id = db.execute("INSERT INTO collectors (email, hash, name, phone_number, address, latitude, longitude) VALUES (?, ?, ?, ?, ?, ?, ?);",
                        email, generate_password_hash(password), request.form.get("name"), request.form.get("phone_number"),
                        request.form.get("address"), float(request.form.get("latitude")), float(request.form.get("longitude")))
        
        # Remember which user has logged in
        session["collector_id"] = id

        flash("Registered!")

        return redirect("/collector/profile")
    else:
        return render_template("collector_register.html")
    

@app.route("/profile", methods=["GET", "POST"])
@user_login_required
def profile():
    """Show user profile"""
    if request.method == "GET":
        # get user info
        user = db.execute("SELECT * FROM users WHERE id = ?;", session["user_id"])[0]

        # get the current tasks that user has
        current_tasks = db.execute("SELECT * FROM tasks JOIN current_tasks ON tasks.id = current_tasks.task_id WHERE current_tasks.user_id = ?;", session["user_id"])

        # get the completed tasks that user has
        completed_tasks = db.execute("SELECT * FROM tasks JOIN completed_tasks ON tasks.id = completed_tasks.task_id WHERE completed_tasks.user_id = ?;", session["user_id"])

        # render the profile page
        return render_template("profile.html", volunteer=user, current_tasks=current_tasks, completed_tasks=completed_tasks)
    else:
        return redirect("/profile")
    

@app.route("/tasks", methods=["GET", "POST"])
@user_login_required
def tasks():
    """Show tasks"""
    if request.method == "GET":
        # get all tasks
        tasks = db.execute("SELECT * FROM tasks;")

        # render the tasks page
        return render_template("tasks.html", tasks=tasks)
    else:
        return redirect("/tasks")
    

@app.route("/tasks/<int:task_id>", methods=["GET", "POST"])
@user_login_required
def task(task_id):
    """Show task"""
    if request.method == "GET":
        # get task
        task = db.execute("SELECT * FROM tasks WHERE id = ?;", task_id)[0]

        # render the task page
        return render_template("task.html", task=task)
    else:
        # add the task to current tasks of the user if it is not already in
        if not db.execute("SELECT * FROM current_tasks WHERE user_id = ? AND task_id = ?;", session["user_id"], task_id):
            db.execute("INSERT INTO current_tasks (user_id, task_id) VALUES (?, ?);", session["user_id"], task_id)

        return redirect("/tasks")
    

if __name__ == '__main__':
    app.run(debug=True)