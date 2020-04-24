import os
from os.path import abspath, dirname
from pathlib import Path

uploads = 'images/'
if not os.path.exists(uploads):
    os.mkdir(uploads)

class Config(object):
    MODEL_PATH = (Path('models/'),'mnist.pkl')
    SECRET_KEY = os.environ.get('SECRET_KEY') or'thisissupersecretkey'
    UPLOAD_FOLDER = uploads
