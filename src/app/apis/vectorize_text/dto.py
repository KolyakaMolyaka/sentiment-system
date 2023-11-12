from flask_restx import Model, fields

tokenlist_model = Model('TokenList', {
	'tokens': fields.List(fields.String, example=['мама', 'мыть', 'рама'], required=True, default=[]),
	'maxWords': fields.Integer(required=False, example=5, default=-1)
})

vectorization_sequence_model = Model('VectorizationSequences', {
	'sequences': fields.List(
		fields.List(
			fields.Integer,
		),
		example=[[2, 4], [3, 4]], required=True
	),
	'dimension': fields.Integer(required=True, example=5)
})

embedding_vectorization_model = Model('EmbeddingVectorization', {
	'tokens': fields.List(fields.String, example=['мама', 'мыть', 'рама'], required=True, default=[]),
	# 'maxReviewLen': fields.Integer(required=True, example=5)
})

