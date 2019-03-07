from flask import Flask, Blueprint
from .state import statebp

app = Flask(__name__)
app.register_blueprint(statebp, url_prefix='/api')
