"""
Air conditiner controller
"""
import os
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)
os.environ["POWER"] = "0"
os.environ['TEMPERATURE'] = "26"


@app.route('/')
def initial():
    temperature = os.getenv('TEMPERATURE')
    return render_template('controller.html', result=temperature)


@app.route('/power')
def power():
    on_off = int(os.getenv('POWER'))
    if on_off:
        os.system('irsend SEND_ONCE aircon power_off')
        os.environ["POWER"] = "0"
    else:
        os.system('irsend SEND_ONCE aircon power_on')
        os.environ["POWER"] = "1"
    return redirect(url_for('initial'))


def temp_limit(temp):
    if temp < 18:
        return 18
    if temp > 30:
        return 30
    return temp


@app.route('/add')
def add_temperature():
    on_off = int(os.getenv('POWER'))
    if on_off:
        temperature = int(os.getenv('TEMPERATURE'))
        os.environ['TEMPERATURE'] = str(temp_limit(temperature + 1))
        # os.system('say temperature up')
    return redirect(url_for('initial'))


@app.route('/minus')
def minus_temperature():
    on_off = int(os.getenv('POWER'))
    if on_off:
        temperature = int(os.getenv('TEMPERATURE'))
        os.environ['TEMPERATURE'] = str(temp_limit(temperature - 1))
        # os.system('say temperature down')
    return redirect(url_for('initial'))


if __name__ == '__main__':
    app.run(debug=True, port=5566)
