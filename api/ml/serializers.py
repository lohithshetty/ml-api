from flask_restplus import fields
from rest_api_ml.api.restplus import api

similar_states = api.model('Similar States', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of the state'),
    'name': fields.String(required=True, description='State name'),
})
