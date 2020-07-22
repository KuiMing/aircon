"""
Air conditiner controller
"""
import os
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
os.environ["POWER"] = "0"

@app.route('/')
def initial():
    return render_template('controller.html')

@app.route('/power')
def power():
    on_off = int(os.getenv('POWER'))
    if on_off:
        os.system('say power off')
        os.environ["POWER"] = "0"
    else:
        os.system('say power on')
        os.environ["POWER"] = "1"
    return redirect(url_for('initial'))

@app.route('/add')
def add_temperature():
    os.system('say temperature up')
    return redirect(url_for('initial'))

@app.route('/minus')
def minus_temperature():
    os.system('say temperature down')
    return redirect(url_for('initial'))

if __name__ == '__main__':
    app.run(debug=True)
