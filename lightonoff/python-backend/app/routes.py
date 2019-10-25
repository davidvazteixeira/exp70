from flask import render_template, redirect
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/toggle')
def toggle():
    if app.serial_is_on:
        app.port.write(b'c')
    return redirect('/index')

