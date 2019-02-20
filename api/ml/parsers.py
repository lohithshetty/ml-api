from flask_restplus import reqparse

arguments = reqparse.RequestParser()
arguments.add_argument('id', type=int, required=True, help='State FIPS ID')
arguments.add_argument('attributes', type=list, required=True, help='Attributes of interest to compare the states')
