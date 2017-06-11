
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
        username = self.request.get("username")
        password = self.request.get("password")
        user = User.login(username, password)
        if user:
            self.login(user)
            return redirect("/")
        else:
            return self.write("WRONG")
    else:
        return render_template('login.html')


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        pass
    else:
        return render_template("signup.html")
