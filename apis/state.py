from .helper_state import supported_attributes, state_id_to_name, get_similar_states
from marshmallow import Schema, fields as ma_fields, post_load, validates_schema, ValidationError
import logging
# from .restful import restful_api as api
from flask_restplus import Resource, fields, marshal_with, Namespace, Api
import json
from flask import Blueprint

log = logging.getLogger(__name__)

statebp = Blueprint('state', __name__)
ns_state = Namespace(
    'similarstate/', description='Get states with simlar Revenue,Tax,Expenditures etc.,')

api = Api(statebp, version='1.0',
          title='TruthTree ML API',
          description='APIs supported by ML')

api.add_namespace(ns_state)

year_range = ns_state.model('Year range',
                            {'start': fields.Integer(default=1977, description="Starting year"),
                             'end': fields.Integer(default=2016, description="Ending year")})

StateSingle = ns_state.model('Similar State for single attribute',
                             {'attribute': fields.String(required=True, description="Attribute Name"),
                              'id': fields.Integer(required=True, description="State ID"),
                              'year_range': fields.Nested(year_range, description="Year Range between 1977 and 2016"),
                              'count': fields.Integer(2, description="Number of similar states in the output")})

StateMulti = ns_state.model('Similar State for multiple attributes',
                            {'id': fields.Integer(required=True, description="State ID"),
                             'attribute': fields.List(fields.String, required=True, description="List of attributes"),
                             'year': fields.Integer(required=True, description="Year"),
                             'count': fields.Integer(2, description="Number of similar states in the output")})


class YearRangeSchema(Schema):
    start = ma_fields.Integer()
    end = ma_fields.Integer()

    @validates_schema
    def validate_input(self, data):
        if data['start'] < 1977 or data['end'] > 2016:
            raise ValidationError(
                "Only years between 1977 and 2016 are supported(inclusive)")


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
                errors['attribute'] = [
                    "Unsupported attribute '{}' ".format(attribute)]
                break
        if data['id'] not in state_id_to_name.keys():
            errors['id'] = ['Invalid State ID']

        if data['year'] < 1977 or data['year'] > 2016:
            errors['year'] = [
                "Only years between 1977 and 2016 are supported(inclusive)"]

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
        List of states which are similar in single attribute.
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
        List of states which are similar in multiple attributes(Total_Revenue,Total_Taxes,etc.,)
        """
        schema = StateMultiSchema()
        result, errors = schema.load(api.payload)
        if errors:
            return errors, 400
        print(json.dumps(result))
        return get_similar_states(result, multi=True)
