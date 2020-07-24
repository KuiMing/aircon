"""
Air conditiner controller
"""
import os
import time
from threading import Thread
from flask import Flask, render_template, redirect, url_for
import Adafruit_DHT

app = Flask(__name__)
os.environ["POWER"] = "0"
os.environ['TEMPERATURE'] = "26"
os.environ['POWERFIGURE'] = "start-button"

def temperature_measurement(model, gpio):
    while True:
        humidity, indoor = Adafruit_DHT.read_retry(model, gpio)
        os.environ["INDOOR"] = indoor
        os.environ['HUMIDITY'] = humidity
        time.sleep(60)

@app.route('/')
def initial():
    temperature = os.getenv('TEMPERATURE')
    os.environ["INDOOR"] = indoor
    power_figure = os.getenv('POWERFIGURE')
    return render_template('controller.html', setting=temperature, indoor=indoor, power=power_figure)


@app.route('/power')
def power():
    on_off = int(os.getenv('POWER'))
    if on_off:
        os.system('irsend SEND_ONCE aircon power_off')
        os.environ["POWER"] = "0"
        os.environ['POWERFIGURE'] = "start-button"
    else:
        os.system('irsend SEND_ONCE aircon power_on')
        os.environ["POWER"] = "1"
        os.environ['POWERFIGURE'] = "start-button-on"
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
    t = Thread(target=temperature_measurement, args=(11, 27))
    t.start()
    app.run(debug=True, port=5566, host='0.0.0.0')
