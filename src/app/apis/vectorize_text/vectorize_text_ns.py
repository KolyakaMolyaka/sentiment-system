from http import HTTPStatus
from flask import jsonify, abort
from flask_restx import Namespace, Resource
from src.app.core.sentiment_analyse.vectorize_text import (
	process_convert_tokens_in_seq_of_codes,
	process_vectorize_sequences,
	process_embeddings_vectorization,
	process_vectorization_info
)

from .dto import vectorization_sequence_model, tokenlist_model, embedding_vectorization_model, vectorization_info_model
from ..utilities.utils import fill_with_default_values

ns = Namespace(
	name='Vectorization Controller',
	description='Взаимодействие с процессом векторизация токенов',
	path='/vectorization/',
	validate=True
)

@ns.route('/vectorization_info')
class VectorizationInfoAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Информация о методе векторизации.')
	@ns.response(int(HTTPStatus.NOT_FOUND), 'Метод векторизации не существует.')
	@ns.expect(vectorization_info_model)
	@ns.doc(description='Получение информации о конкретном методе векторизации.')
	def post(self):
		""" Получение подробной информации о конкретном методе векторизации """
		d = ns.payload

		vectorization_title = d.get('vectorizationTitle')

		vectorization_description = process_vectorization_info(vectorization_title)

		response = jsonify({
			'vectorization_title': vectorization_title,
			'description': vectorization_description
		})
		response.status_code = HTTPStatus.OK

		return response

@ns.route('/convert_tokens_in_codes')
class VectorizationAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Последовательность кодов для токенов и мета-дата.')
	@ns.expect(tokenlist_model)
	@ns.doc(
		description='Преобразование токенов в список кодов. '
					'Сначала выбираются наиболее встречающиеся слова. '
					'Учтите, что в системе используются два специальных кода: '
					'0 - код заполнитель, 1 - код неизвестного слова. '
					'Вы получите последовательность, которая будет определять ваши токены в виде списка кодов.'
	)
	def post(self):
		""" Преобразование токенов в список кодов """

		fill_with_default_values(ns.payload, tokenlist_model)
		d = ns.payload

		tokens = d.get('tokens')
		max_words = -1

		seq, word_to_index, index_to_word = process_convert_tokens_in_seq_of_codes(tokens, max_words)
		response = jsonify({
			'sequence': seq,
			'wordToIndex': word_to_index,
			'indexToWord': index_to_word
		})
		response.status_code = HTTPStatus.OK

		return response


@ns.route('/vectorize_sequences')
class VectorizationSequenceAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Векторизованные последовательности.')
	@ns.response(int(HTTPStatus.BAD_REQUEST), 'Пользователь ввел неправильные параметры.')
	@ns.expect(vectorization_sequence_model)
	@ns.doc(
		description='Мешок слов это вектор, который содержит столько элементов (dimension), сколько слов анализируется. '
					'Каждый элемент вектора соответствует определенному слову, а значение вектора равно '
					'количеству раз, когда слово встречается в тексте.'
	)
	def post(self):
		''' Векторизация последовательности с помощью алгоритма "Мешок слов" '''

		fill_with_default_values(ns.payload, vectorization_sequence_model)
		d = ns.payload

		sequence = d.get('sequences')
		dimension = d.get('dimension')

		if dimension <= 0:
			response = jsonify({
				'error': "'dimension' параметр не может быть <= 0."
			})
			response.status_code = HTTPStatus.BAD_REQUEST
			return response

		vectorized_sequences = process_vectorize_sequences(sequence, dimension)
		response = jsonify({
			'vectorizedSequences': vectorized_sequences
		})
		response.status_code = HTTPStatus.OK

		return response


@ns.route('/embedding_vectorize_text')
class EmbeddingVectorizationAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Плотные векторные представления.')
	@ns.expect(embedding_vectorization_model)
	@ns.doc(
		description='Получение плотного векторного представления токенов при помощи модели Navec.'
					'Каждому токену соответствует вектор, элементы которого являются вещественными числами.'
	)
	def post(self):
		""" Получение плотных векторных представлений из токенов """

		d = ns.payload
		tokens = d.get('tokens')
		max_review_len = len(tokens)

		embeddings = process_embeddings_vectorization(tokens, max_review_len)
		embeddings = [[float(num) for num in vect]
					  for vect in embeddings]
		response = jsonify({
			'embeddings': embeddings,
		})
		response.status_code = HTTPStatus.OK

		return response

