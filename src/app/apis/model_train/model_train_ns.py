from http import HTTPStatus
from flask import jsonify
from flask_restx import Resource, Namespace
from src.app.core.train_model.train_model_logic import train_model_logic
import pandas as pd

from .dto import train_model
from src.app.core.auth.auth_logic import requires_auth
ns = Namespace(
	name='Model Train Controller',
	description='Обучение модели',
	path='/model_train/',
	validate=True
)


@ns.route('/train_with_teacher')
class ModelTrainWithTeatherAPI(Resource):
	method_decorators = [requires_auth]

	@ns.response(int(HTTPStatus.BAD_REQUEST), 'Не совпадает число комментариев с числом классов.')
	@ns.expect(train_model)
	@ns.doc(
		desctiption='Обучение модели с учителем.'
	)
	@ns.doc(security='basicAuth')
	def post(self):
		""" Обучение модели МО с учителем согласно заданным параметрам """

		from ..utilities import utils
		utils.fill_with_default_values(ns.payload, train_model)
		d = ns.payload

		# данные для сохранения модели
		model_title = d.get('modelTitle')

		# данные для токенизации
		tokenizer_type = d.get('tokenizerType')
		stop_words = d.get('stopWords')
		use_default_stop_words = d.get('useDefaultStopWords')

		# данные для векторизации
		vectorization_type = d.get('vectorizationType')

		if vectorization_type == 'bag-of-words':
			# проверка, что есть
			# maxWords
			# showUnknownWordCodeInVectors
			pass

		# данные для классификатора
		classifier = d.get('classifier')

		comments = d.get('comments')
		classes = d.get('classes')

		max_words = d.get('maxWords')
		min_token_len = d.get('minTokenLength')
		delete_numbers_flag = d.get('deleteNumbers')
		excluded_default_stop_words = d.get('excludeDefaultStopWords')


		if len(comments) != len(classes):
			response = jsonify({
				'error': 'Число комментариев не совпадает с числом классов.'
			})
			response.status_code = HTTPStatus.BAD_REQUEST
			return response

		for c in classes:
			if c not in (0, 1):
				response = jsonify({
					'error': 'Классы могут быть только 0 - отрицательный, 1 - положительный.'
				})
				response.status_code = HTTPStatus.BAD_REQUEST
				return response

		train_info = list(zip(comments, classes))
		df = pd.DataFrame(train_info, columns=['text', 'score'])
		trained_meta = train_model_logic(df, tokenizer_type, stop_words, use_default_stop_words,
										 vectorization_type, model_title, classifier,
										 max_words, classes, comments, min_token_len,
										 delete_numbers_flag, excluded_default_stop_words)
		response = jsonify({
			 **trained_meta
		})
		response.status_code = HTTPStatus.OK

		return response
