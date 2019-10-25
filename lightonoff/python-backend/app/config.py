import os, random

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or str(random.random()).replace('.', '')
