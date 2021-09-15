import sqlite3
from cs50 import SQL
from flask import Flask, flash, redirect, render_template
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, usd
import os
#Flask configuration 
app = Flask(__name__)

#Auto reload templates 
app.config["TEMPLATES_AUTO_RELOAD"] = True

code = os.urandom(24)
app.secret_key = code

#db = SQL("sqlite:///budget.db")

@app.route("/")
def index():
    """Show transaction history"""

    return render_template("/index.html")