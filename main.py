
from flask import Flask, render_template, request, redirect, url_for, flash, \
                    make_response, jsonify
#   imports for authentication
from flask import session as login_session
import random
import string
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

phrase = "That'sGold,Jerry.GOLD!"
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
        return self.response.headers.add_header(
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
        secured_cookie = self.request.cookies.get(name)
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
        user = User.login(username, password)
        if user:
            self.login(user)
            return redirect("/")
        else:
            return self.write("WRONG")
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
                    new_user = User(name=username, pass_hash=password, email=email)
                    new_user.put()
                    return redirect("/")
        else:
            return redirect('/login')
    else:
        a = User.query()
        for u in a:
            print u
        return render_template("signup.html")
