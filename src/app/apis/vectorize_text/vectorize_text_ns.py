from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource
from src.app.core.sentiment_analyse.vectorize_text import (
	process_convert_tokens_in_seq_of_codes,
	process_vectorize_sequences,
	process_embeddings_vectorization
)

from .dto import vectorization_sequence_model, tokenlist_model, embedding_vectorization_model
from ..utilities.utils import fill_with_default_values

ns = Namespace(
	name='Vectorization Controller',
	description='Векторизация токенов',
	path='/vectorization/',
	validate=True
)


@ns.route('/convert_tokens_in_codes')
class VectorizationAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Последовательность кодов для токенов и мета-дата.')
	@ns.expect(tokenlist_model)
	@ns.doc(
		description='Преобразование токенов в список кодов. '
					'Сначала выбираются наиболее встречающиеся слова. '
					'Вы можете ограничить список слов используя параметр maxWords. '
					'Вы получите последовательность, которая будет определять ваши токены в виде списка кодов.'
	)
	def post(self):
		""" Преобразование токенов в список кодов """

		fill_with_default_values(ns.payload, tokenlist_model)
		d = ns.payload

		tokens = d.get('tokens')
		max_words = d.get('maxWords')

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
		description='Мешок слов это вектор, который содержит столько элементов, сколько слов анализируется. '
					'Каждый элемент вектора соответствует определенному слову, а значение вектора равно количеству раз, когда слово встречается в тексте.'

	)
	def post(self):
		""" Vectorize sequence using Bag Of Words Algorithm """
		""" Векторизация последовательности с помощью алгоритма 'Мешок слов'"""

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
	@ns.response(int(HTTPStatus.OK), 'Embeddings vectors')
	@ns.expect(embedding_vectorization_model)
	@ns.doc(
		description='Получение векторного представления текста при помощи модели Navec.'
	)
	def post(self):
		""" Получение плотных векторных представлений из токенов """

		d = ns.payload
		tokens = d.get('tokens')
		# max_review_len = d.get('maxReviewLen')
		max_review_len = len(tokens)

		embeddings = process_embeddings_vectorization(tokens, max_review_len)
		embeddings = [[float(num) for num in vect]
					  for vect in embeddings]
		response = jsonify({
			'embeddings': embeddings
		})
		response.status_code = HTTPStatus.OK

		return response
