import os
import logging.config
from app import app

logging_conf_path = os.path.normpath(
    os.path.join(os.path.dirname(__file__), 'logging.conf'))
logging.config.fileConfig(logging_conf_path)
log = logging.getLogger(__name__)


if __name__ == "__main__":
    app.config.from_object(os.environ['APP_SETTINGS'])
    app.run()
