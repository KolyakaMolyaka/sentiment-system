from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource
from .dto import tokenization_info_reqparser
from src.app.core.sentiment_analyse.tokenize_text import (
	process_text_tokenization
)

ns = Namespace(
	name='Tokenization Controller',
	description='Работа с токенизацией',
	path='/tokenization/',
	validate=True
)


@ns.route('/tokenize_text')
class TokenizeTextAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Tokens of text')
	@ns.expect(tokenization_info_reqparser)
	def post(self):
		""" Tokenize text """
		d = tokenization_info_reqparser.parse_args()
		text = d.get('text')

		# validate stop words
		stop_words = d.get('stopWords')
		if stop_words:
			stop_words = stop_words[0]
			for el in stop_words:
				if not isinstance(el, str):
					response = jsonify({
						'error': f'{el} is not an string'
					})
					response.status_code = HTTPStatus.CONFLICT
					return response
		else:
			stop_words = None

		# get tokens with used stop words
		tokens, used_stop_words = process_text_tokenization(text, stop_words=stop_words)
		response = jsonify({
			'tokens': tokens,
			'usedStopWords': list(used_stop_words)
		})
		response.status_code = HTTPStatus.OK

		return response
