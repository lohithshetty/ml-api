import os
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

POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASS = os.getenv("POSTGRES_PASS", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")


SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(POSTGRES_USER, POSTGRES_PASS, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB)
SQLALCHEMY_TRACK_MODIFICATIONS = True
