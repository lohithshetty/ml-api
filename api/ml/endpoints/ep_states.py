import logging

from flask import request
from flask_restplus import Resource, fields, marshal_with
from api.restplus import api
from api.ml.serializers import *
from api.ml.similar_states import *
import json

log = logging.getLogger(__name__)

ns = api.namespace('ml/similarstates', description='Get states which have simlar Revenue,Tax,Expenditures etc.,')


@ns.route('/supported')
@ns.response(500, 'Internal Server Error')
class Supported(Resource):
    def get(self):
        """
        Returns list of attributes supported to compare states
        """
        return {'supported_attributes': supported_attributes}


@ns.route('/<int:id>/<string:attribute>')
@ns.response(404, 'State not found.')
class SimilarStates(Resource):
    @ns.marshal_with(similar_states, envelope='similar_states')
    def get(self, id, attribute):
        """
        Returns list of states which are similar in the attribute of interest
        """
        response, response_code = get_similar_states(id, attribute)
        return response, response_code
    # get.__schema__ = {'id': 'int', 'attribute': 'string'}
