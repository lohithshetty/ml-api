import logging.config

import os
from flask import Flask, Blueprint
from api.ml.serializers import ns_state
import db
from api.restplus import api
from flask_script import Manager
 
app = Flask(__name__)
# TODO have a basedir and use that as reference
logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
manager = Manager(app)

def initialize_app(flask_app):
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    api.add_namespace(ns_state)
    # api.add_namespace(ns_supported)
    # app.url_map.converters['list'] = ListConverter

    flask_app.register_blueprint(blueprint)

if __name__ == "__main__":
    db.init_db()
    initialize_app(app)
    manager.run()
