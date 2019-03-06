import logging
import traceback

from flask_restplus import Api
from sqlalchemy.orm.exc import NoResultFound


log = logging.getLogger(__name__)


api = Api(version='1.0', title='TruthTree ML API',
          description='APIs supported by ML')


@api.errorhandler
def default_error_handler(e):
    message = 'Unhandled exception!!'
    log.exception(message)

    return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'No Result Found'}, 404
