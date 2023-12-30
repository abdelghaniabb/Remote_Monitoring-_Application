#!/usr/bin/python3

import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from country_list import countries_for_language
from werkzeug.security import check_password_hash, generate_password_hash


from helpers import login_required, apology, strong_password
from gpio import change_gpio, get_state_gpio



# Configure application
app = Flask(__name__)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///information.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



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
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/logout")
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
        # get registration information
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        establishment = request.form.get("establishment")
        sector = request.form.get("sector")
        phone = request.form.get("phone")
        contry = request.form.get("contry")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # check registration information
        users_dict = db.execute("SELECT username FROM users")
        users = list()
        for item in users_dict:
            users.append(item['username'])

        if email in users:
            return apology("username already exists")
        if password != confirmation:
            return apology("passwords do not match")
        if not strong_password(password):
            return apology("Not a Strong password")

        # save registration information
        _hash = generate_password_hash(password)
        db.execute("INSERT INTO users (username, hash) VALUES ('{}', '{}');".format(email, _hash))
        db.execute("INSERT INTO users_information (first_name, last_name, email, establishment, sector, phone, contry) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');".format(first_name, last_name, email, establishment, sector, phone, contry))

        return render_template("registered.html", first_name=first_name)
    else:
        countries = list()
        for key, value in dict(countries_for_language('en')).items():
            countries.append(value)
        
        return render_template("register.html", countries=countries)


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """account settings"""
    user_id = int(session.get("user_id"))
    if request.method == "POST":
        # Get user's information for the registration
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Check statements
        if not username:
            return apology("No username entered")
        
        users_dict = db.execute("SELECT username FROM users WHERE id = {};".format(user_id))

        if username != users_dict[0]['username']:
            return apology("wrong username")
        if not password or not confirmation:
            return apology("No password entered")
        if password != confirmation:
            return apology("passwords do not match")
        if not strong_password(password):
            return apology("Not a Strong password")

        # save registration information
        _hash = generate_password_hash(password)
        db.execute("UPDATE users SET hash = '{}' WHERE id = {};".format(_hash, user_id))

        return render_template("password.html")
    
    else:
        return render_template("settings.html")



@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/light")
@login_required
def light():
    return render_template("light.html")

@app.route("/gpio1", methods=["GET", "POST"])
@login_required
def gpio1():
    if request.method == "POST":
        if request.form.get('status') == "true":
            """turn ON the gpio 15"""
            change_gpio(15, 1)
        else:
            change_gpio(15, 0)
        
        return "done"
    else:
        if get_state_gpio(15):
            status = "true"
        else:
            status = "false"
        return str(status)

@app.route("/gpio2", methods=["GET", "POST"])
@login_required
def gpio2():
    if request.method == "POST":
        if request.form.get('status') == "true":
            """turn ON the gpio 16"""
            change_gpio(16, 1)
        else:
            change_gpio(16, 0)
        
        return "done"
    else:
        if get_state_gpio(16):
            status = "true"
        else:
            status = "false"
        return str(status)

@app.route("/gpio3", methods=["GET", "POST"])
@login_required
def gpio3():
    if request.method == "POST":
        if request.form.get('status') == "true":
            """turn ON the gpio 22"""
            change_gpio(22, 1)
        else:
            change_gpio(22, 0)
        
        return "done"
    else:
        if get_state_gpio(22):
            status = "true"
        else:
            status = "false"
        return str(status)


@app.route("/temperature")
@login_required
def temperature():
    """get the lab temperature"""
    data = db.execute("SELECT temperature, humidity, date FROM temperature ORDER BY date DESC LIMIT 1;")
    humidity = data[0]['humidity']
    temperature = data[0]['temperature']
    return render_template("temperature.html", humidity=humidity, temperature=temperature)


@app.route("/camera")
@login_required
def camera():
    """live camera"""
    return render_template("camera.html")

@app.route("/history", methods=["GET", "POST"])
@login_required
def history():
    """history of the temperature"""
    if request.method == "POST":
        date = request.form.get("date")
        if not date:
            return apology("no date entered")
        data = db.execute("SELECT temperature, humidity, date FROM temperature WHERE DATE(date) = '{}' ORDER BY date DESC;".format(date))
        return render_template("history.html", data=data)
    else:
        data = db.execute("SELECT temperature, humidity, date FROM temperature ORDER BY date DESC LIMIT 30;")
        return render_template("history.html", data=data)


app.run(host='0.0.0.0', port=None)