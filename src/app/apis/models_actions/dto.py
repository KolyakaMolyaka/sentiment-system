from flask_restx import Model, fields


user_ml_model = Model('UserMlModel', {
	'modelTitle': fields.String(required=True, example='my_model')
})

user_prediction_model = Model('UserPredictionMlModel', {
	'text': fields.String(required=True, example='Красивая рубашка'),
	'modelTitle': fields.String(required=True, example='my_model'),
})

user_prediction_model_v2 = Model('UserPredictionMlModelv2', {
	'modelTitle': fields.String(required=True, example='my_model'),
	'vector': fields.List(fields.Float(required=True), example=[.2, .4])
})
