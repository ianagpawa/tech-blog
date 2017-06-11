
from flask import Flask, render_template, request, redirect, url_for, flash, \
                    make_response, jsonify
#   imports for authentication
from flask import session as login_session
import random
import string

import json
from functools import wraps

import Post

from google.appengine.ext import ndb

app = Flask(__name__)

@app.route('/')
def front():
    return render_template("base.html")
