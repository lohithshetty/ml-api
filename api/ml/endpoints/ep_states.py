import logging

from flask import request
from flask_restplus import Resource, fields, marshal_with
from api.restplus import api
from api.ml.serializers import *
from api.ml.similar_states import *
import json
from marshmallow import Schema, fields as ma_fields, post_load, validates_schema, ValidationError

log = logging.getLogger(__name__)


class YearRangeSchema(Schema):
    start = ma_fields.Integer()
    end = ma_fields.Integer()

    @validates_schema
    def validate_input(self, data):
        if data['start'] < 1977 or data['end'] > 2016:
            raise ValidationError("Only years between 1977 and 2016 are supported(inclusive)")


class StateSingleSchema(Schema):
    id = ma_fields.Integer()
    attribute = ma_fields.String()
    count = ma_fields.Integer()
    year_range = ma_fields.Nested(YearRangeSchema)

    @validates_schema
    def validate_input(self, data):
        errors = {}
        if data['attribute'] not in supported_attributes:
            errors['attribute'] = ['Unsupported attribute']
        if data['id'] not in state_id_to_name.keys():
            errors['id'] = ['Invalid State ID']

        if errors:
            raise ValidationError(errors)

    class Meta:
        fields = ('id', 'attribute', 'count', 'year_range')
        ordered = True


class StateMultiSchema(Schema):
    id = ma_fields.Integer()
    attribute = ma_fields.List(ma_fields.String)
    count = ma_fields.Integer()
    year = ma_fields.Integer()

    @validates_schema
    def validate_input(self, data):
        pass
        errors = {}
        for attribute in data['attribute']:
            if attribute not in supported_attributes:
                errors['attribute'] = ["Unsupported attribute '{}' ".format(attribute)]
                break
        if data['id'] not in state_id_to_name.keys():
            errors['id'] = ['Invalid State ID']

        if data['year'] < 1977 or data['year'] > 2016:
            errors['year'] = ["Only years between 1977 and 2016 are supported(inclusive)"]

        if errors:
            raise ValidationError(errors)

        class Meta:
            fields = ('id', 'attribute', 'count', 'year')
            ordered = True


@ns_state.route('/supported')
@ns_state.response(500, 'Internal Server Error')
class Supported(Resource):
    def get(self):
        """
        Returns list of attributes supported to compare states
        """
        return {'supported_attributes': supported_attributes}


@ns_state.route('/single')
@ns_state.response(404, 'State not found.')
class SimilarStates(Resource):
    @api.expect(StateSingle)
    def post(self):
        """
        Returns list of states which are similar in the attribute of interest
        """
        schema = StateSingleSchema()
        result, errors = schema.load(api.payload)
        if errors:
            return errors, 400
        return get_similar_states(result)


@ns_state.route('/multi')
@ns_state.response(404, 'State not found.')
class SimilarStatesMulti(Resource):
    @api.expect(StateMulti)
    def post(self):
        """
        Returns list of states which are similar in the attribute of interest
        """
        schema = StateMultiSchema()
        result, errors = schema.load(api.payload)
        if errors:
            return errors, 400
        print(json.dumps(result))
        return get_similar_states(result, multi=True)
