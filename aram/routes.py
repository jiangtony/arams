from flask import render_template, request
from aram import app

@app.route("/")
def home():
    return render_template('index.html')
