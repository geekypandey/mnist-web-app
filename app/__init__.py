#Rule : Always validate the input on server side.Always.Don't trust the user!
from flask import Flask
from flask_bootstrap import Bootstrap
from config import Config


app = Flask(__name__)

app.config.from_object(Config)
bootstrap = Bootstrap(app)

from app import routes


