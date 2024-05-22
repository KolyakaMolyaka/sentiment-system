from flask_restx import Model, fields


user_ml_model = Model('UserMlModel', {
	'modelTitle': fields.String(required=True, example='my_model')
})

tokenization_model = Model('Tokenization', {
	'tokenizerType': fields.String(required=True,
								   enum=('nltk-tokenizer', 'default-whitespace-tokenizer'),
								   example='nltk-tokenizer'),
	'text': fields.String(required=True, example='Это текст для токенизации'),
	'stopWords': fields.List(fields.String, example=['ешкин-кот', 'блин'], required=False, default=None),
	'useDefaultStopWords': fields.Boolean(example=True, default=True, required=False)
})
