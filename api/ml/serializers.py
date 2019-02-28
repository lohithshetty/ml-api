from flask_restplus import fields
from api.restplus import api


similar_states = api.model('Similar States', {
    'state_id': fields.Integer(readOnly=True, description='The unique identifier of the state'),
    'attribute_name': fields.String(required=True, description='State name'),
})

# model = api.model('Model', {
#     'supported': fields.String,
# })

# similar_states = api.model('Resource', {
#     'name': fields.String,
#     'id': fields.Integer
# })
# # similar_states = {
# #     fields.List(fields.Nested(similar_state)),
# # }
