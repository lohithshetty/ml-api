import os
# Flask settings
FLASK_SERVER_NAME = 'ml.api:8080'
# TODO: Set it to Fasle in production
FLASK_DEBUG = True

# Flask-Restplus settings
RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
RESTPLUS_VALIDATE = True
RESTPLUS_MASK_SWAGGER = False
RESTPLUS_ERROR_404_HELP = False

# SQLAlchemy settings

PGHOST = os.getenv("PGHOST", "localhost")
PGPORT = os.getenv("PGPORT", 5432)
PGUSER = os.getenv("PGUSER", "postgres")
PGPASSWORD = os.getenv("PGPASSWORD", 123)
PGDATABASE = os.getenv("PGDATABASE", "data")

SQLALCHEMY_DATABASE_URI = "postgresql://{}:{}@{}:{}/{}".format(PGUSER, PGPASSWORD, PGHOST, PGPORT, PGDATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = True
