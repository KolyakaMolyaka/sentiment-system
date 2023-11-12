from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource
from src.app.core.sentiment_analyse.vectorize_text import (
	process_convert_tokens_in_seq_of_codes
)

from .dto import tokenlist_model
from ..utilities.utils import fill_with_default_values

ns = Namespace(
	name='Vectorization Controller',
	description='Работа с векторизацией',
	path='/vectorization/',
	validate=True
)


@ns.route('/convert_tokens_in_codes')
class VectorizationAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Sequence of codes for given tokens and meta data')
	@ns.expect(tokenlist_model)
	def post(self):
		""" Convert tokens in sequence of codes """

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



