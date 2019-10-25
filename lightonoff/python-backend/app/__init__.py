from flask import Flask
from .config import Config
import serial

app = Flask(__name__, static_url_path='/static')
app.config.from_object(Config)
app.serial_is_on = True

if app.serial_is_on:
    bauld = 115200
    dev = '/dev/ttyACM0'
    app.port = serial.Serial(dev, bauld, timeout=1)
    print(app.port)

from app import routes
