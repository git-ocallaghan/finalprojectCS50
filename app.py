import sqlite3
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask import sessions
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, usd
import os
#Flask configuration 
app = Flask(__name__)

#Auto reload templates 
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Check Configuration section for more details
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

code = os.urandom(24)
app.secret_key = code



db = SQL("sqlite:///budget.db")

@app.route("/")
def index():
    """Show transaction history"""

    return render_template("/index.html")

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
        