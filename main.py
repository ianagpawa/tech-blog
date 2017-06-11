
from flask import Flask, render_template, request, redirect, url_for, flash, \
                    make_response, jsonify
#   imports for authentication
from flask import session as login_session
import random
import string

import json
from functools import wraps

from Post import Post

from google.appengine.ext import ndb

app = Flask(__name__)

def login_required(func):
    '''
    login_required: function decorator for checking if user is logged in
    Returns:
        If not logged in, redirects to login page.
    '''
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'email' in login_session:
            return func(*args, **kwargs)
        else:
            flash("You are not allowed to acces this without logging in!")
            return redirect("/login")
    return decorated_function



@app.route('/')
def front():
    posts = Post.query()

    return render_template("front.html", posts=posts)


@app.route("/new/", methods=['GET', 'POST'])
@login_required
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
