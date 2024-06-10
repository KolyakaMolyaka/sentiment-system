from flask_restx import Model, fields
from . import classes_list, comments_list

available_classifiers = ('logistic-regression',)

train_model = Model('TrainInfo', {
	'modelTitle': fields.String(required=True, example='my_model'),
	'classifier': fields.String(required=True, example='logistic-regression',
								enum=available_classifiers
								),
	'tokenizerType': fields.String(required=True,
								   enum=('nltk-tokenizer', 'default-whitespace-tokenizer', 'wordpunct-tokenizer'),
								   example='nltk-tokenizer'),
	'vectorizationType': fields.String(required=True,
									   enum=('bag-of-words', 'embeddings'),
									   example='embeddings'),
	'stopWords': fields.List(fields.String, example=['ешкин-кот', 'блин'], required=False, default=None),
	'useDefaultStopWords': fields.Boolean(example=True, default=True, required=False),
	'excludeDefaultStopWords': fields.List(fields.String, example=[], required=False, default=None),
	'punctuations': fields.List(fields.String, required=True, example=list('!?,.;:') + ['..', '...'],
								default=list('!?,.;:') + ['..', '...']),
	'minTokenLength': fields.Integer(example=1, default=1, required=False),
	'deleteNumbers': fields.Boolean(example=False, default=False, required=False),
	'comments': fields.List(fields.String, example=comments_list, required=True),
	'classes': fields.List(fields.Integer(help='0 - Negative, 1 - Positive'), example=classes_list,
						   required=True),
	'maxWords': fields.Integer(required=True, example=400, default=400),

})

train_model_v2 = Model('TrainInfov2', {
	'modelTitle': fields.String(required=True, example='my_model'),
	'classifier': fields.String(required=True, example=available_classifiers[0], enum=available_classifiers),
	'vectors': fields.List(
		fields.List(
			fields.Float,
		),
		example=[[.1, .2], [.2, .4], [.3, .4], [.2, .3], [.4, .5], [.3, .5]], required=True
	),
	'classes': fields.List(fields.Integer(help='0 - Negative, 1 - Positive'), example=[1, 0, 1, 1, 0, 0], required=True),
})