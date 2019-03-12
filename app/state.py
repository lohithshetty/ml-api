from app.helper_state import place, get_similar_places
from marshmallow import Schema, fields as ma_fields, post_load, validates_schema, ValidationError
import logging
from flask_restplus import Resource, fields, marshal_with, Namespace, Api
import json
from flask import Blueprint

log = logging.getLogger(__name__)

placebp = Blueprint('place', __name__)
ns_place = Namespace(
    'similar', description='Get places with simlar Revenue,Tax,Expenditures etc.,')

api = Api(placebp, version='1.0',
          title='TruthTree ML API',
          description='APIs supported by ML')

api.add_namespace(ns_place)

year_range = ns_place.model('Year range',
                            {'start': fields.Integer(default=1977, description="Starting year"),
                             'end': fields.Integer(default=2016, description="Ending year")})

PlaceSingle = ns_place.model('Similar places for single attribute',
                             {'attribute': fields.String(required=True, description="Attribute Name"),
                              'normalize_by': fields.String(description="Attribute to normalize the data. Ex. Population, Total_Revenue", default="Population"),
                              'id': fields.Integer(required=True, description="Place ID"),
                              'year_range': fields.Nested(year_range, description="Year Range between 1977 and 2016"),
                              'count': fields.Integer(2, description="Number of similar places in the output")})

PlaceMulti = ns_place.model('Similar places for multiple attributes',
                            {'id': fields.Integer(required=True, description="Place ID"),
                             'attribute': fields.List(fields.String, required=True, description="List of attributes"),
                             'normalize_by': fields.String(description="Attribute to normalize the data. Ex. Population, Total_Revenue", default="Population"),
                             'year': fields.Integer(required=True, description="Year"),
                             'count': fields.Integer(2, description="Number of similar places in the output")})


class YearRangeSchema(Schema):
    start = ma_fields.Integer()
    end = ma_fields.Integer()

    @validates_schema
    def validate_input(self, data):
        if data['start'] < 1977 or data['end'] > 2016:
            raise ValidationError(
                "Only years between 1977 and 2016 are supported(inclusive)")


class PlaceSingleSchema(Schema):
    id = ma_fields.Integer()
    attribute = ma_fields.String()
    count = ma_fields.Integer()
    year_range = ma_fields.Nested(YearRangeSchema)

    @validates_schema
    def validate_input(self, data):
        errors = {}
        if data['attribute'] not in place.supported_attributes:
            errors['attribute'] = ['Unsupported attribute']
        if data['id'] not in place.id_to_name.keys():
            errors['id'] = ['Invalid Place ID']

        if errors:
            raise ValidationError(errors)

    class Meta:
        fields = ('id', 'attribute', 'count', 'year_range')
        ordered = True


class PlaceMultiSchema(Schema):
    id = ma_fields.Integer()
    attribute = ma_fields.List(ma_fields.String)
    count = ma_fields.Integer()
    year = ma_fields.Integer()

    @validates_schema
    def validate_input(self, data):
        pass
        errors = {}
        for attribute in data['attribute']:
            if attribute not in place.supported_attributes:
                errors['attribute'] = [
                    "Unsupported attribute '{}' ".format(attribute)]
                break
        if data['id'] not in place.id_to_name.keys():
            errors['id'] = ['Invalid Place ID']

        if data['year'] < 1977 or data['year'] > 2016:
            errors['year'] = [
                "Only years between 1977 and 2016 are supported(inclusive)"]

        if errors:
            raise ValidationError(errors)

        class Meta:
            fields = ('id', 'attribute', 'count', 'year')
            ordered = True


@ns_place.route('/supported')
@ns_place.response(200, 'OK')
@ns_place.response(500, 'Internal Server Error')
class Supported(Resource):
    def get(self):
        """
        Returns list of attributes supported to compare places
        """
        return {'attributes_supported': place.supported_attributes}


@ns_place.route('/single')
@ns_place.response(501, 'Place ID not supported')
@ns_place.response(500, 'Internal Server Error')
@ns_place.response(200, 'OK')
@ns_place.response(400, 'Bad Request')
class SimilarPlaces(Resource):
    @api.expect(PlaceSingle)
    def post(self):
        """
        List of places which are similar in single attribute.
        """
        schema = PlaceSingleSchema()
        result, errors = schema.load(api.payload)
        if errors:
            return errors, 400
        return get_similar_places(result)


@ns_place.route('/multi')
@ns_place.response(501, 'Place ID not supported')
@ns_place.response(500, 'Internal Server Error')
@ns_place.response(200, 'OK')
@ns_place.response(400, 'Bad Request')
class SimilarPlacesMulti(Resource):
    @api.expect(PlaceMulti)
    def post(self):
        """
        List of places which are similar in multiple attributes(Total_Revenue,Total_Taxes,etc.  
        """
        schema = PlaceMultiSchema()
        result, errors = schema.load(api.payload)
        if errors:
            return errors, 400
        print(json.dumps(result))
        return get_similar_places(result, multi=True)
