from flask_restx import Model, fields
from flask_restx.reqparse import RequestParser

""" DTO """
input_to_output_model = Model('ModelInputToOutput', {
	'y_true': fields.List(fields.String, required=True, example=[
		'positive', 'negative', 'negative',
		'positive', 'positive', 'positive',
		'negative']),
	'y_pred': fields.List(fields.String, required=True, example=[
		'positive', 'negative', 'positive',
		'positive', 'negative', 'positive',
		'positive'
	]),
	'positive_label': fields.String(required=True, example='positive')
})
