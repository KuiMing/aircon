"""
Air conditiner controller
"""
from datetime import datetime
import os
import time
from threading import Thread
from flask import Flask, render_template, redirect, url_for, jsonify
import Adafruit_DHT

app = Flask(__name__)
os.environ["POWER"] = "0"
os.environ['TEMPERATURE'] = "26"
os.environ['POWERFIGURE'] = "start-button"
os.environ['AIRCONAUTO'] = "0"


@app.route('/indoor_temperature')
def temperature_measurement():
    _, indoor = Adafruit_DHT.read_retry(11, 27)
    return jsonify(result=indoor)


@app.route('/')
def initial():
    temperature = os.getenv('TEMPERATURE')
    _, indoor = Adafruit_DHT.read_retry(11, 27)
    power_figure = os.getenv('POWERFIGURE')
    auto_mode = int(os.getenv('AIRCONAUTO'))
    mode = 'AUTO' if auto_mode else ""
    return render_template(
        'controller.html',
        setting=temperature,
        indoor=indoor,
        power=power_figure,
        mode=mode)


@app.route('/power')
def power():
    on_off = int(os.getenv('POWER'))
    if on_off:
        os.system('irsend SEND_ONCE aircon power_off')
        os.environ["POWER"] = "0"
        os.environ['POWERFIGURE'] = "start-button"
        os.environ['AIRCONAUTO'] = "0"
    else:
        os.system('irsend SEND_ONCE aircon power_on')
        os.environ["POWER"] = "1"
        os.environ['POWERFIGURE'] = "start-button-on"
    return redirect(url_for('initial'))


def temperature_detector():
    _, indoor = Adafruit_DHT.read_retry(11, 27)
    while indoor < 30 and os.getenv('POWER') == '0' and datetime.now(
    ).hour >= 3 and datetime.now().hour <= 5:
        _, indoor = Adafruit_DHT.read_retry(11, 27)
        time.sleep(10)
    os.system('irsend SEND_ONCE aircon power_on')
    os.environ["POWER"] = "1"


@app.route('/auto')
def auto():
    on_off = int(os.getenv('AIRCONAUTO'))
    if on_off:
        os.environ["AIRCONAUTO"] = "0"
    else:
        os.environ["AIRCONAUTO"] = "1"
        os.environ['POWERFIGURE'] = "start-button-on"
        thread = Thread(target=temperature_detector)
        thread.start()
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
        temperature = temp_limit(temperature + 1)
        os.environ['TEMPERATURE'] = str(temperature)
        os.system('irsend SEND_ONCE aircon aircon_{}'.format(temperature))
    return redirect(url_for('initial'))


@app.route('/minus')
def minus_temperature():
    on_off = int(os.getenv('POWER'))
    if on_off:
        temperature = int(os.getenv('TEMPERATURE'))
        temperature = temp_limit(temperature - 1)
        os.environ['TEMPERATURE'] = str(temperature)
        os.system('irsend SEND_ONCE aircon aircon_{}'.format(temperature))
    return redirect(url_for('initial'))


if __name__ == '__main__':
    app.run(debug=True, port=5566, host='0.0.0.0')
