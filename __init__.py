# __init__.py
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/poker')
def poker():
    return render_template('poker.html')

@app.route('/hexGame')
def hex_game():
    return render_template('hexGame.html')
