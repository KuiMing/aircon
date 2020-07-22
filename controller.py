"""
Air conditiner controller
"""
import os
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
os.environ["POWER"] = "0"
os.environ['TEMPERATURE'] = "28"

@app.route('/')
def initial():
    temperature = os.getenv('TEMPERATURE')
    return render_template('controller.html', result=temperature)

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
    on_off = int(os.getenv('POWER'))
    if on_off:
        os.system('say temperature up')
        temperature = int(os.getenv('TEMPERATURE'))
        os.environ['TEMPERATURE'] = str(temperature + 1)
    return redirect(url_for('initial'))

@app.route('/minus')
def minus_temperature():
    on_off = int(os.getenv('POWER'))
    if on_off:
        os.system('say temperature down')
        temperature = int(os.getenv('TEMPERATURE'))
        os.environ['TEMPERATURE'] = str(temperature - 1)
    return redirect(url_for('initial'))

if __name__ == '__main__':
    app.run(debug=True)
