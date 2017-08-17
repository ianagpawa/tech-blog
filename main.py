
from flask import Flask, render_template, request, redirect, url_for, flash, \
                    make_response, jsonify, session, escape

import random
import string
import hashlib
import re
import json

from string import letters
from functools import wraps

from Post import Post
from User import User

from google.appengine.ext import ndb
from google.appengine.api import memcache
from google.appengine.datastore.datastore_query import Cursor

from listing import website as website

app = Flask(__name__)
app.secret_key = 'IsThatYouJohnWayne?'


@app.context_processor
def project_titles():
    titles = Post.query(projection=[Post.project], group_by=[Post.project])
    return dict(titles=titles)


@app.route('/', methods=["GET", "POST"])
def front():

    if 'username' in session:
        username = session['username']
        state = True
    else:
        state = False

    posts = Post.query().order(-Post.created)

    items = 10

    cursors = memcache.get("cursors")
    if not cursors:
        cursors_list = [None]
        more = True
        cur = None
        while more:
            thing, cur, more = posts.fetch_page(items, start_cursor=cur)
            cursors_list.append(cur)

        cursors_list.pop()

        memcache.set('cursors', cursors_list)
        cursors = memcache.get("cursors")

    if request.method == "POST":
        if request.form['page']:

            value = request.form['page']
            value = int(value) - 1
            cursor = cursors[value]

            posts, cur, more = posts.fetch_page(items, start_cursor=cursor)

            return render_template('front.html', posts=posts, state=state, cursors=cursors)

    else:
        posts, cur, more = posts.fetch_page(items)
        return render_template("front.html", posts=posts, state=state, cursors=cursors)


@app.route("/new/", methods=['GET', 'POST'])
def newPost():
    if 'username' in session and session['username'] == 'Ian':
        if request.method == "POST":
            if request.form['title'] and request.form['content']:
                title = request.form['title']
                content = request.form['content']
                project = request.form['project']
                pj_link = website[project]
                github = request.form['github-link']
                creator = "Ian Agpawa"
                post = Post(title=title,
                            content=content,
                            project=project,
                            project_link=pj_link,
                            github=github,
                            creator=creator)
                post.put()
                memcache.set('cursors', None)
                return redirect("/")

        else:
            return render_template("new_post.html", state=True)
    else:
        return redirect("/")



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

                return redirect("/")
            else:
                return redirect("/login")
        else:
            #   Change to redirect to signup later if needed
            return redirect("/")
    else:
        return render_template("login.html")




@app.route("/logout/", methods=["GET", "POST"])
def logout():
    session.pop("username", None)
    return redirect("/")


@app.route("/post/<int:post_id>/")
def showPost(post_id):
    post = Post.get_by_id(post_id)
    if 'username' in session and session['username'] == 'Ian':
        return render_template('post_L.html', post=post, state=True)
    else:
        return render_template('post.html', post=post)



@app.route('/post/<int:post_id>/edit/', methods=["GET", "POST"])
def editPost(post_id):
    post = Post.get_by_id(post_id)
    if 'username' in session and session['username'] == 'Ian':
        if request.method == "POST":
            if request.form['change-title'] and request.form['change-content']:
                title = request.form['change-title']
                post.title = title

                content = request.form['change-content']
                post.content = content

                project = request.form['change-project']
                post.project = project

                pjLink = request.form['change-pj-link']
                post.project_link = pjLink

                github = request.form['change-github']
                post.github = github

                post.put()

                return redirect(url_for("showPost", post_id = post_id))


        else:
            return render_template("edit_post.html", post=post, state=True)
    else:
        return redirect('/')


@app.route('/post/<int:post_id>/delete/', methods=["GET", "POST"])
def deletePost(post_id):
    post = Post.get_by_id(post_id)
    if 'username' in session and session['username'] == "Ian":
        if request.method == "POST":
            if request.form['delete_post']:
                post.key.delete()
                return redirect("/")
        else:
            return render_template('delete_post.html', state=True)
    else:
        return redirect("/")



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
                    session['username'] = username
                    return redirect("/")
        else:
            return redirect('/login')
    else:
        return render_template("signup.html")

def camelCase(word):
    return word[0].capitalize() + word[1:].lower()

@app.route("/projects/<string:project_name>/")
def projectPosts(project_name):
    if 'username' in session:
        username = session['username']
        state = True
    else:
        state = False

    name = project_name.split("_")
    if len(name) > 1:
        name = list(map(lambda word: camelCase(word), name))
    project = " ".join(name)
    posts = Post.query()
    posts = posts.filter(Post.project == project)
    if posts.count() > 0:
        posts = posts.order(-Post.created)
    else:
        posts = False
    return render_template("project.html", posts=posts, project=project, state=state)


@app.route("/projects/<string:project_name>/JSON/")
def projectPostsJSON(project_name):
    name = project_name.split("_")
    if len(name) > 1:
        name = list(map(lambda word: camelCase(word), name))
    project = " ".join(name)
    posts = Post.query()
    posts = posts.filter(Post.project == project)
    posts = posts.order(-Post.created)
    # for post in posts:
    #     a = json.loads(post.serialize)
    #     print a
    return jsonify(Posts=[json.loads(post.serialize) for post in posts])
