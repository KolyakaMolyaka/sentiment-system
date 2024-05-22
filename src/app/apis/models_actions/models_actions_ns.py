from http import HTTPStatus
from flask import jsonify, request
from flask_restx import Namespace, Resource
from .dto import tokenization_model, user_ml_model
from src.app.ext.database.models import MlModel, User
from src.app.core.auth.auth_logic import requires_auth
from src.app.core.model_actions.model_actions_logic import process_model_delete_request
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
		# utils.fill_with_default_values(ns.payload, tokenization_model)
		# d = ns.payload

		# Parse payload to get data
		# text = d.get('text')
		# use_default_stop_words = d.get('useDefaultStopWords')
		# stop_words = d.get('stopWords')
		# tokenizer_type = d.get('tokenizerType')

		# get tokens with used stop words
		# tokens, used_stop_words = process_text_tokenization(
		# 	tokenizer_type,
		# 	text,
		# 	stop_words=stop_words,
		# 	use_default_stop_words=use_default_stop_words
		# )

		# return tokens with used stop words

		user = User.get(request.authorization.username)
		models = MlModel.query.filter_by(user_id=user.id)
		output_models = [{'model_title': m.model_title, 'model_accuracy': m.model_accuracy} for m in models]
		response = jsonify({
			# 'tokens': tokens,
			# 'usedStopWords': list(used_stop_words)
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
