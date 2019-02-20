# Flask settings
FLASK_SERVER_NAME = 'localhost:5000'
# TODO: Set it to Fasle in production
FLASK_DEBUG = True  

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:123@localhost:5432/data"
SQLALCHEMY_TRACK_MODIFICATIONS = True
