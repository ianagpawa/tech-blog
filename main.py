from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def front():
    return render_template("base.html")
