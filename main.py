
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

@app.route('/')
def front():
    # posts = ndb.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
    book = self.request.get('default')
    ancestor_key = ndb.Key("Post", book)
    posts = Post.query()

    return render_template("front.html", posts=posts)
