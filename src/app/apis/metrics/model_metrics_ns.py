from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource, marshal
from src.app.core.metrics.model_metrics_logic import process_user_get_model_metrics
from .dto import input_to_output_model

model_metrics_ns = Namespace(
	name='Model Metrics Controller',
	description='Получение метрик модели машинного обучения',
	path='/model/metrics/',
	validate=True
)


@model_metrics_ns.route('/')
class ModelMetrics(Resource):

	@model_metrics_ns.response(int(HTTPStatus.OK), 'Метрики вычислены.')
	@model_metrics_ns.expect(input_to_output_model)
	def post(self):
		"""Получение основных метрик модели машинного обучения."""
		request_data = model_metrics_ns.payload

		y_true: [str] = request_data.get('y_true')
		y_pred: [str] = request_data.get('y_pred')
		positive_label: str = request_data.get('positive_label')

		metrics = process_user_get_model_metrics(y_true, y_pred, positive_label)

		response = jsonify(metrics)
		response.status_code = HTTPStatus.OK

		return response
