from flask_restx import Model, fields

train_model = Model('TrainInfo', {
	'modelTitle': fields.String(required=True, example='my_model'),
	'classifier': fields.String(required=True, example='logistic-regression',
								enum=('logistic-regression',)
								),
	'tokenizerType': fields.String(required=True,
								   enum=('nltk-tokenizer', 'default-whitespace-tokenizer'),
								   example='nltk-tokenizer'),
	'vectorizationType': fields.String(required=True,
								   enum=('bag-of-words', 'embeddings'),
								   example='embeddings'),
	'stopWords': fields.List(fields.String, example=['ешкин-кот', 'блин'], required=False, default=None),
	'useDefaultStopWords': fields.Boolean(example=True, default=True, required=False),
	'comments': fields.List(fields.String, example=[
		'Не видел такой дырявой рубашки',
		'Хорошая рубашка, красивый цвет. Микровельвет. Под майку отлично. Большемерит сильно. На свой 44 взяла xs и тот большой. Но оставила. Такого цвета больше не нашла у других пролавцов',
		'Качество ужас,очень длинная !!!!',
		'Хорошая рубашка',
		'Отличная рубашка ❤️',
		'Качество ужас,очень длинная !!!!',
		'Это не рубашка а фильм ужасов.',
		'на рост 165 немного большая, но все равно забрала. для тех кто хочет чуть побольше, то берите',
		'Шикарно. Но я взяла на размер меньше.',
		'Не стоит своих денег, ткань, покрой, пошив оставляет желать лучшего.'
	], required=True),
	'classes': fields.List(fields.Integer(help='0 - Negative, 1 - Positive'), example=[0, 1, 0, 1, 1, 0, 0, 1, 1, 0],
						   required=True),
	'maxWords': fields.Integer(required=True, example=40, default=40),

})
