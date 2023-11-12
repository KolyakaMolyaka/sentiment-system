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
		# tokenization_type = d.get('tokenizationType')

		tokens = process_text_tokenization(text)
		response = jsonify({
			'tokens': tokens
		})
		response.status_code = HTTPStatus.OK

		return response
