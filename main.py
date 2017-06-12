
from flask import Flask, render_template, request, redirect, url_for, flash, \
                    make_response, jsonify
#   imports for authentication
from flask import session as login_session
import random
import string
import hashlib
from string import letters


import re
import json
from functools import wraps

from Post import Post
from User import User

from google.appengine.ext import ndb

app = Flask(__name__)



@app.route('/')
def front():
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





phrase = "DontYourPutThatEvilOnMeRickyBobby"
def make_secure(unsecured):
    """
    make_secure: method for creating a secure password keyed-hash using HMAC
                and a pass phrase.
    Args:
        unsecured (data type: str): string input of user's unsecure password
    Returns:
        returns concatenated string of HMAC keyed-hash password and
            unsecured password
    """
    return '%s|%s' % (hmac.new(phrase, unsecured).hexdigest(), unsecured)



def check_secure(secured_pass):
    """
    make_secure: method for creating a secure password keyed-hash using HMAC
                and a pass phrase.
    Args:
        secured_pass (data type: str): string input of user's hashed password
    Returns:
        True if the secured_pass matches the unsecured password substring after
        it has been hashed.
    """
    unsecured = secured_pass.split('|')[1]
    if secured_pass == make_secure(unsecured):
        return unsecured




@app.route("/login/", methods=["GET", 'POST'])
def login():


    def set_secure_cookie(self, name, value):
        """
        set_secure_cookie:  Method for setting a secure cookie.
        Args:
            name (data type: str): Name of a cookie.
            value (data type: str): Value of a cookie
        """
        secured_cookie = make_secure(value)
        return response.headers.add_header(
            'Set-Cookie',
            "%s=%s; Path=/" % (name, secured_cookie)
        )


    def read_secure_cookie(self, name):
        """
        read_secure_cookie:     Method for reading a secure cookie.
        Args:
            name (data type: str): Name of a cookie
        Returns:
            True or False
        """
        secured_cookie = request.cookies.get(name)
        return secured_cookie and check_secure(secured_cookie)

    def login(self, user):
        """
        login:  Method for logging a user in.
        Args:
            user_id (data type: str):   The user key id.
        """
        user_id = str(user.key().id())
        return self.set_secure_cookie('user_id', user_id)


    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query()
        user = user.filter(User.name == username).fetch()

        print user[0]
        if len(user) > 0:
            name = user[0].name
            pass_hash = user[0].pass_hash

            if username == name and valid_pass(name, password, pass_hash):
                return redirect("/")
            else:
                return redirect("/login")
        else:
            return render_template("signup.html")
        # user = User.login(username, password)
        # if user:
        #     self.login(user)
        #     return redirect("/")
        # else:
        #     return redirect("/signup")
    else:
        return render_template('login.html')



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


@app.route("/signup", methods=["GET", "POST"])
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
