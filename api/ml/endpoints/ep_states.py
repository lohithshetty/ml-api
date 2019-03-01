import logging

from flask import request
from flask_restplus import Resource, fields, marshal_with
from api.restplus import api
from api.ml.serializers import *
from api.ml.similar_states import *
import json
from marshmallow import Schema, fields as ma_fields, post_load, validates_schema, ValidationError


log = logging.getLogger(__name__)

ns_state = api.namespace('state/', description='Get states with simlar Revenue,Tax,Expenditures etc.,')
ns_county = api.namespace('county/', description='Get the list of supported attributes')

year_range = ns_state.model('Year range',
                            {'start': fields.Integer(default=1977, description="Starting year"),
                             'end': fields.Integer(default=2016, description="Ending year")})

SS = ns_state.model('Similar State',
                    {'attribute': fields.String(required=True, description="Attribute Name"),
                     'id': fields.Integer(required=True, description="State ID"),
                     'years': fields.Nested(year_range, description="Year Range between 1977 and 2016"),
                     'count': fields.Integer(2)})


class YearRangeSchema(Schema):
    start = ma_fields.Integer()
    end = ma_fields.Integer()

    @validates_schema
    def validate_input(self, data):
        if data['start'] < 1977 or data['end'] > 2016:
            raise ValidationError("Only years between 1977 and 2016 are supported(inclusive)")


class SSSchema(Schema):
    attribute = ma_fields.String()
    count = ma_fields.Integer()
    id = ma_fields.Integer()
    years = ma_fields.Nested(YearRangeSchema)

    @validates_schema
    def validate_input(self, data):
        errors = {}
        if data['attribute'] not in supported_attributes:
            errors['attribute'] = ['Unsupported attribute']
        if data['id'] not in state_id_name_map.keys():
            errors['id'] = ['Invalid State ID']

        if errors:
            raise ValidationError(errors)


@ns_state.route('/supported')
@ns_state.response(500, 'Internal Server Error')
class Supported(Resource):
    def get(self):
        """
        Returns list of attributes supported to compare states
        """
        return {'supported_attributes': supported_attributes}


@ns_state.route('/similarstates/')
@ns_state.response(404, 'State not found.')
class SimilarStates(Resource):
    @api.expect(SS)
    def post(self):
        """
        Returns list of states which are similar in the attribute of interest
        """
        schema = SSSchema()
        result, errors = schema.load(api.payload)
        if errors:
            return errors, 400
        return get_similar_states(result)
