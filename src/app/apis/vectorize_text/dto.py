from flask_restx import Model, fields

tokenlist_model = Model('TokenList', {
	'tokens': fields.List(fields.String, example=['мама', 'мыть', 'рама'], required=True, default=[]),
	'maxWords': fields.Integer(required=False, example=5, default=-1)
})
