import shutil
import tempfile
import os
from http import HTTPStatus
from flask import jsonify, request, send_file, abort, current_app
from flask_restx import Namespace, Resource
from .dto import user_ml_model, user_prediction_model, user_prediction_model_v2
from src.app.ext.database.models import MlModel, User, Tokenizer, Vectorization
from src.app.core.auth.auth_logic import requires_auth
from src.app.core.model_actions.model_actions_logic import process_model_delete_request, \
	process_model_prediction_request, process_model_prediction_with_vector_request

ns = Namespace(
	name='Models Actions Controller',
	description='Взаимодействие с созданными пользователем моделями',
	path='/models_actions/',
	validate=True
)


@ns.route('/models')
class ModelsInfoAPI(Resource):
	method_decorators = [requires_auth]

	@ns.response(int(HTTPStatus.OK), 'Список обученных моделей пользователя.')
	@ns.doc(
		description='Получение списка обученных моделей пользователя с подробной информацией.'
	)
	@ns.doc(security='basicAuth')
	def get(self):
		""" Получение списка обученных моделей  """
		db_user = User.get(request.authorization.username)
		models = db_user.ml_models
		print(f'Модели пользователя "{db_user.username}":', [m.model_title for m in models])

		from .models_info_template import SelfTrainedModelInfo, AlgorithmTrainedModelInfo
		output_models = []
		for db_model in models:
			if db_model.trained_self:
				model_info:dict = SelfTrainedModelInfo(db_model).get_info()
			else:
				model_info:dict = AlgorithmTrainedModelInfo(db_model).get_info()
			output_models.append(model_info)

		response = jsonify({
			'models': output_models
		})
		response.status_code = HTTPStatus.OK

		return response

	@ns.response(int(HTTPStatus.OK), 'Указанная модель успешно удалена.')
	@ns.doc(description='Удаление ранее обученной модели пользователя.')
	@ns.expect(user_ml_model)
	@ns.doc(security='basicAuth')
	def delete(self):
		""" Удаление ранее обученной модели """
		d = ns.payload
		# Parse payload to get data
		model_title = d.get('modelTitle')

		process_model_delete_request(model_title)

		response = jsonify({'message': 'модель успешно удалена'})
		response.status_code = HTTPStatus.OK
		return response


@ns.route('/download_model')
class DownloadModelAPI(Resource):
	method_decorators = [requires_auth]

	@ns.response(int(HTTPStatus.OK), 'Исходные файлы обученной модели.')
	@ns.response(int(HTTPStatus.NOT_FOUND), 'Указанная модель не найдена.')
	@ns.expect(user_ml_model)
	@ns.doc(description='Получение исходных файлов ранее обученной модели в виде ZIP-архива.')
	@ns.doc(security='basicAuth')
	def post(self):
		""" Получение исходных файлов обученной модели """
		d = ns.payload
		model_title = d.get('modelTitle')

		user = User.query.filter_by(username=request.authorization.username).one_or_none()
		model = MlModel.query.filter_by(user_id=user.id, model_title=model_title).one_or_none()

		if not model:
			abort(int(HTTPStatus.NOT_FOUND), f'модель {model_title} не существует')

		output_filename = 'ml_model'
		dir_name = os.path.join(current_app.config['TRAINED_MODELS'], user.username, model_title)

		# Создание временного архива
		with tempfile.TemporaryDirectory() as temp_dir:
			temp_archive_path = shutil.make_archive(os.path.join(temp_dir, output_filename), 'zip', dir_name)
			return send_file(temp_archive_path, mimetype="application/octet-stream", as_attachment=True)


@ns.route('/model_prediction/v1')
class ModelsPredictionAPIv1(Resource):
	method_decorators = [requires_auth]

	@ns.response(int(HTTPStatus.OK), 'Предсказание модели')
	@ns.response(int(HTTPStatus.NOT_FOUND), 'Указанная модель не найдена.')
	@ns.response(int(HTTPStatus.CONFLICT), 'Данная модель обучалась не с помощью алгоритма, доступного в системе.')
	@ns.expect(user_prediction_model)
	@ns.doc(security='basicAuth', description='Получение предсказания обученной модели.')
	def post(self):
		""" Предсказание тональности с помощью доступного в системе алгоритма на основе обученной модели """
		d = ns.payload

		# Parse payload to get data
		model_title = d.get('modelTitle')
		text = d.get('text')

		prediction = process_model_prediction_request(model_title, text)[0]
		sentiment = get_sentiment(prediction)
		response = jsonify(sentiment)
		response.status_code = HTTPStatus.OK
		return response


@ns.route('/model_prediction/v2')
class ModelPredictionAPIv2(Resource):
	method_decorators = [requires_auth]

	@ns.response(int(HTTPStatus.OK), 'Предсказание модели')
	@ns.response(int(HTTPStatus.NOT_FOUND), 'Указанная модель не найдена.')
	@ns.response(int(HTTPStatus.CONFLICT), 'Данная модель обучалась с помощью алгоритма, доступного в системе.')
	@ns.expect(user_prediction_model_v2)
	@ns.doc(security='basicAuth',
			description=\
					'Для получения предсказания обученной модели пользователь вводит вектор с количеством признаков '
					'(размерностью), используемой при обучении модели. Каждый элемент вектора представляет степень '
					'выраженности i-го признака.'
	)
	def post(self):
		""" Предсказание тональности на основе модели, обученной с помощью подготовленных пользователем векторов """
		d = ns.payload

		# Parse payload to get data
		model_title = d.get('modelTitle')
		vector = d.get('vector')

		prediction = process_model_prediction_with_vector_request(model_title, vector)[0]
		sentiment = get_sentiment(prediction)
		response = jsonify(sentiment)
		response.status_code = HTTPStatus.OK
		return response


def get_sentiment(prediction):
	negative_accuracy, positive_accuracy = prediction

	if abs(negative_accuracy - positive_accuracy) <= 0.05:
		prediction_result = 'нейтральная тональность'
	elif negative_accuracy > positive_accuracy:
		prediction_result = 'негативная тональность'
	else:
		prediction_result = 'позитивная тональность'

	print('neg - pos = ', abs(negative_accuracy - positive_accuracy))
	print('prediction', prediction)

	return {
		'предсказание': prediction_result,
		'точность позитивной тональности согласно модели': positive_accuracy,
		'точность негативной тональности согласно модели': negative_accuracy,
	}
