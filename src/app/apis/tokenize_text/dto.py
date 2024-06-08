from flask_restx import Model, fields

tokenization_model = Model('Tokenization', {
	'tokenizerType': fields.String(required=True,
								   enum=('nltk-tokenizer', 'default-whitespace-tokenizer', 'wordpunct-tokenizer'),
								   example='nltk-tokenizer'),
	'text': fields.String(required=True, example='Хорошая рубашка, красивый цвет. Микровельвет. Под майку отлично. Большемерит сильно. На свой 44 взяла xs и тот большой. Но оставила. Такого цвета больше не нашла у других пролавцов'),
	'stopWords': fields.List(fields.String, example=['ешкин-кот', 'блин'], required=False, default=None),
	'useDefaultStopWords': fields.Boolean(example=True, default=True, required=False),
	'minTokenLength': fields.Integer(example=1, default=1, required=False),
	'deleteNumbers': fields.Boolean(example=False, default=False, required=False)
})

tokenizer_info_model = Model('TokenizerInfoModel', {
	'tokenizerTitle': fields.String(required=True,
								   enum=('nltk-tokenizer', 'default-whitespace-tokenizer', 'wordpunct-tokenizer'),
								   example='nltk-tokenizer'),
})

