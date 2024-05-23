from http import HTTPStatus
from flask import jsonify, request, send_file, abort
from flask_restx import Namespace, Resource
from .dto import user_ml_model, user_prediction_model
from src.app.ext.database.models import MlModel, User
from src.app.core.auth.auth_logic import requires_auth
from src.app.core.model_actions.model_actions_logic import process_model_delete_request, process_model_prediction_request
# from src.app.core.sentiment_analyse.tokenize_text import (
# 	process_text_tokenization
# )
from ..utilities import utils

ns = Namespace(
	name='Models Actions Controller',
	description='Взаимодействие с моделями',
	path='/models_actions/',
	validate=True
)


@ns.route('/models')
class ModelsInfoAPI(Resource):
	method_decorators = [requires_auth]

	@ns.response(int(HTTPStatus.OK), 'Модели пользователя')
	# @ns.expect(tokenization_model)
	@ns.doc(
		description='Получение информации об обученных моделях пользователя.'
	)
	@ns.doc(security='basicAuth')
	def get(self):
		""" Обученные модели """
		user = User.get(request.authorization.username)
		# models = MlModel.query.filter_by(user_id=user.id)
		models = user.ml_models
		print(f'{user.username} модели:', [m.model_title for m in models])
		output_models = [
			{'model_title': m.model_title,
			 'model_tokenizer_type': m.tokenizer_type,
			 'model_vectorization_type': m.vectorization_type,
			 'model_use_default_stop_words': m.use_default_stop_words,
			 'model_accuracy': m.model_accuracy,
			 'model_precision': m.model_precision,
			 'model_recall': m.model_recall,
			 } for m in models]
		response = jsonify({
			'models': output_models
		})
		response.status_code = HTTPStatus.OK

		return response

	@ns.response(int(HTTPStatus.OK), 'Удаление модели пользователя')
	@ns.doc(description='Удаление модели пользователя')
	@ns.expect(user_ml_model)
	@ns.doc(security='basicAuth')
	def delete(self):
		""" Удаление обученной модели """
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

	@ns.response(int(HTTPStatus.OK), 'Модели пользователя')
	@ns.expect(user_ml_model)
	@ns.doc(description='Загрузка полученной модели.')
	@ns.doc(security='basicAuth')
	def post(self):
		""" Получение исходных файлов модели """
		d = ns.payload
		model_title = d.get('modelTitle')

		user = User.query.filter_by(username=request.authorization.username).one_or_none()
		model = MlModel.query.filter_by(user_id=user.id, model_title=model_title)

		if not model:
			abort(int(HTTPStatus.NOT_FOUND), f'модель {model_title} не существует')

		import shutil
		output_filename = 'ml_model'

		dir_name = f'/usr/src/app/src/app/core/train_model/models/{user.username}/{model_title}'
		archive = shutil.make_archive(output_filename, 'zip', dir_name)
		print(archive)
		return send_file(archive, mimetype="application/octet-stream", as_attachment=True)



@ns.route('/model_prediction')
class ModelsPredictionAPI(Resource):
	method_decorators = [requires_auth]
	@ns.response(int(HTTPStatus.OK), 'Предсказание модели')
	@ns.doc(description='Получение предсказания обученной модели.')
	@ns.expect(user_prediction_model)
	@ns.doc(security='basicAuth')
	def post(self):
		""" Предсказание тональности на основе обученной модели  """
		d = ns.payload

		# Parse payload to get data
		model_title = d.get('modelTitle')
		text = d.get('text')

		prediction = process_model_prediction_request(model_title, text)[0]
		negative_accuracy, positive_accuracy = prediction

		if abs(negative_accuracy - positive_accuracy) <= 0.05:
			prediction_result = 'нейтральная тональность'
		elif negative_accuracy > positive_accuracy:
			prediction_result = 'негативная тональность'
		else:
			prediction_result = 'позитивная тональность'

		print('neg - pos = ', abs(negative_accuracy - positive_accuracy))
		print('prediction', prediction)

		response = jsonify({'предсказание': prediction_result,
							'точность позитивной тональности согласно модели': positive_accuracy,
							'точность негативной тональности согласно модели': negative_accuracy,
							})
		response.status_code = HTTPStatus.OK
		return response
