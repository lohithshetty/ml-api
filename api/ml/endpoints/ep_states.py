import logging

from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.ml.similar_states import *

log = logging.getLogger(__name__)

ns = api.namespace('ml/similarstates', description='Get similar states with similar revenue growth, similar spendings, etc.,')


@ns.route('/supported')
@api.response(500, 'Internal Server Error')
class Supported(Resource):

    def get(self):
        """
        Returns list of attributes supported to compare states
        """
        return {"supported": supported}


@ns.route('/<int:id>/<string:attribute>')
@api.response(404, 'State not found.')
class SimilarStates(Resource):

    def get(self, id, attribute):
        """
        Returns list of states which are similar in the attribute of interest
        """
        return get_similar_states(id, attribute)
