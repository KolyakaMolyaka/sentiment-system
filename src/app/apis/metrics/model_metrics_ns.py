from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource, marshal
from src.app.core.metrics.model_metrics_logic import process_user_get_model_metrics, process_user_calculate_model_metrics
from src.app.core.auth.auth_logic import requires_auth
from .dto import input_to_output_model, ml_model_metrics

model_metrics_ns = Namespace(
	name='Model Metrics Controller',
	description='Получение метрик модели машинного обучения',
	path='/model/metrics/',
	validate=True
)


@model_metrics_ns.route('/calculate_metrics')
class ModelMetrics(Resource):

	@model_metrics_ns.response(int(HTTPStatus.OK), 'Метрики вычислены.')
	@model_metrics_ns.expect(input_to_output_model)
	@model_metrics_ns.doc(
		description=\
				'Вычисление основных метрик качества модели: accuracy, precision, recall, confusion_matrix. '
				'Элементы confusion matrix сопоставляются согласно следующей схеме: [0][0] - True Positive, '
				'[0][1] - False Negative, [1][0] - False Positive, [1][1] - True Negative.'

	)
	def post(self):
		"""Вычисление основных метрик модели машинного обучения на основе правильных и предсказанных значений."""
		request_data = model_metrics_ns.payload

		y_true: [str] = request_data.get('y_true')
		y_pred: [str] = request_data.get('y_pred')
		positive_label: str = request_data.get('positive_label')

		metrics = process_user_get_model_metrics(y_true, y_pred, positive_label)

		response = jsonify(metrics)
		response.status_code = HTTPStatus.OK

		return response


@model_metrics_ns.route('/get_model_metrics')
class ModelMetricsAPI(Resource):
	method_decorators = [requires_auth]
	@model_metrics_ns.response(int(HTTPStatus.OK), 'Метрики модели.')
	@model_metrics_ns.expect(ml_model_metrics)
	@model_metrics_ns.doc(
		description='Получение основных метрик модели машинного обучения по названию. Флаг getFromDb '
					'позволяет получить метрики из БД или рассчитать их заново (в т.ч. confusion matrix). '
					'Флаг saveInDb сохраняет вновь рассчитанные метрики в БД.',
		security='basicAuth'
	)
	def post(self):
		""" Получение основных метрик модели машинного обучения по названию модели """
		request_data = model_metrics_ns.payload

		model_title = request_data.get('modelTitle')
		get_from_db_flag = request_data.get('getFromDb')
		save_in_db_flag = request_data.get('saveInDb')

		metrics = process_user_calculate_model_metrics(model_title, get_from_db_flag, save_in_db_flag)

		response = jsonify({
			'metrics': metrics
		})
		response.status_code = HTTPStatus.OK
		return response



		return 'ok'