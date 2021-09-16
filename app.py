import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask import sessions
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helpers import apology, login_required, usd

#Flask configuration 
app = Flask(__name__)

#Auto reload templates 
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Check Configuration section for more details
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///budget.db")

@app.route("/")
@login_required
def index():
    #Home page
    user_id = session["user_id"]

    current_balance = db.execute("SELECT account_balance FROM users WHERE id = ?", user_id)[0]['account_balance']
    print(current_balance)

    return render_template("/index.html",current_balance=usd(current_balance))

@app.route("/login", methods=["GET", "POST"])
def login():
#Log the user in 
    session.clear()

    if request.method == "POST":
        
        if not request.form.get("username"):
            return apology("Please enter a valid username",403)
        
        elif not request.form.get("password"):
            return apology("This is an incorrect password", 403)
        
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("Invalid username and/or password", 403)
        
        session["user_id"] = rows[0]["id"]

        return redirect("/")
    
    else:
        return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        
        if not username:
            return apology("You must provide a username", 403)
        
        elif not password:
            return apology("You must provide a password ", 403)

        elif not confirmation:
            return apology("Please confirm your password", 403)

        elif not password == confirmation:
            return apology("You password is not matching")
        
        hash = generate_password_hash(password)

        try:
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", username, hash)
            
            return redirect("/")
        
        except:
            return apology("Username is already taken")
        
    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
        