#!/bin/sh
xset -dpms s off
cd /home/pi/Downloads/exp70/thermohygrometer/python_backend
python3 backend.py &
