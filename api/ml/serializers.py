from flask_restplus import fields
from api.restplus import api

ns_state = api.namespace('similarstate/', description='Get states with simlar Revenue,Tax,Expenditures etc.,')
ns_county = api.namespace('similarcounty/', description='Get the list of supported attributes')


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
