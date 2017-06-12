
from flask import Flask, render_template, request, redirect, url_for, flash, \
                    make_response, jsonify, session, escape
#   imports for authentication
import random
import string
import hashlib
import hmac
from string import letters


import re
import json
from functools import wraps

from Post import Post
from User import User

from google.appengine.ext import ndb

app = Flask(__name__)
app.secret_key = 'IsThatYouJohnWayne?'


@app.route('/')
def front():
    if 'username' in session:
        username = session['username']
        print username
    posts = Post.query()
    return render_template("front.html", posts=posts)


@app.route("/new/", methods=['GET', 'POST'])
def newPost():
    if request.method == "POST":
        if request.form['title'] and request.form['content']:
            title = request.form['title']
            content = request.form['content']
            post = Post(title=title, content=content)
            post.put()
            return redirect("/")

    else:
        return render_template("new_post.html")




@app.route("/login/", methods=["GET", 'POST'])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query()
        user = user.filter(User.name == username).fetch()

        if len(user) > 0:
            user = user[0]
            name = user.name
            pass_hash = user.pass_hash
            if username == name and valid_pass(name, password, pass_hash):
                session['username'] = username
                return redirect(url_for('front'))
            else:
                return redirect("/login")
        else:
            return render_template("signup.html")
    else:
        return render_template('login.html')




@app.route("/logout/", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    return redirect("/")

    

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

PASSWORD_RE = re.compile(r"^.{3,20}$")

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
    """
    valid_username: Method for checking if a user name is valid.
    Args:
        username (data type: str):  A user's name.
    Returns:
        True or False
    """
    return username and USER_RE.match(username)


def valid_password(password):
    """
    valid_password: Method for checking if a user password is valid.
    Args:
        password (data type: str):  A user's password.
    Returns:
        True or False
    """
    return password and PASSWORD_RE.match(password)


def valid_email(email):
    """
    valid_email: Method for checking if a user's email is valid.
    Args:
        email (data type: str):  A user's email.
    Returns:
        True or False.
    """
    return not email or EMAIL_RE.match(email)




def make_salt():
    """
    make_salt:  Method for creating salt string for use of hashing user
                passwords.
    Returns:
        Random string of length five.
    """
    string = ''
    for x in range(0,5):
        string += random.choice(letters)
    return string


def make_pass_hash(name, password, salt = None):
    """
    make_pass_hash: Method for creating password hash.
    Args:
        name (data type: str): String of user's name.
        password (data type: str): String of user's password.
        salt (data type: str): Sting of random five characters.
    Returns:
        A string hashed with the password and a random salt string.
    """
    if not salt:
        salt = make_salt()
    hashed = hashlib.sha256(name + password + salt).hexdigest()
    return '%s|%s' % (hashed, salt)


def valid_pass(name, password, hashed):
    """
    valid_pass: Method for checking if a hashed string matches the string of a
                user's password after it has been hashed.
    Args:
        name (data type: str): User's name
        password (data type: str): User's password
        hashed (data type: str) Hashed password
    """
    salt = hashed.split('|')[1]
    return hashed == make_pass_hash(name, password, salt)


@app.route("/signup/", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        if request.form['username'] and request.form['password']:
            username = request.form["username"]
            password = request.form["password"]
            verify = request.form['verify']
            email = request.form["email"]
            params = dict(username=username, email=email)

            if not valid_username(username):
                params['error_username'] = "Not a valid username."

            if not valid_password(password):
                params["error_password"] = "Not a valid password."
            elif password != verify:
                params['error_verify'] = "Your passwords don't match."

            if not valid_email(email):
                params['error_email'] = "Not a valid email."

            if len(params) > 2:
                return render_template("signup.html", **params)
            else:
                user = User.query()
                user = user.filter(User.name == username).fetch()
                if len(user) > 0:
                    error_message = "User already exists."
                    return render_template("signup.html", error_username = error_message)
                else:
                    pass_hash = make_pass_hash(username, password)
                    new_user = User(name=username, pass_hash=pass_hash, email=email)
                    new_user.put()
                    return redirect("/")
        else:
            return redirect('/login')
    else:
        return render_template("signup.html")
