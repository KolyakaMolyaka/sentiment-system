from flask_restx import fields, Model

sentiment_model = Model('Sentiment', {
	'modelType': fields.String(
		required=True,
		enum=('bag-of-words', 'embeddings'),
		example='bag-of-words'
	),
	'text': fields.String(
		required=True,
		example='Хорошая рубашка, красивый цвет. Микровельвет. Под майку отлично. Большемерит сильно. '
				'На свой 44 взяла xs и тот большой. Но оставила. Такого цвета больше не нашла у других пролавцов'
	),
})
