from flask_restplus import Api
from flask import Blueprint

blueprint = Blueprint('api', __name__)
restful_api = Api(blueprint,
                  version='1.0',
                  title='TruthTree ML API',
                  description='APIs supported by ML')
