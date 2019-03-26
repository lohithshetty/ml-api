from flask import Flask
import os
from flask import Flask, Blueprint


def create_app(test_config=None):
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__, instance_relative_config=True)

    if test_config:
        # load the test config if passed in
        app.config.update(test_config)
    else:
        app.config.from_object(os.environ['APP_SETTINGS'])

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from app import db
    # db.init_db()
    # apply the blueprints to the app
    from app import endpoints
   # from app import city
    app.register_blueprint(endpoints.placebp, url_prefix='/api')
    # app.register_blueprint(city.citybp, url_prefix='/api')

    return app


app = create_app()
