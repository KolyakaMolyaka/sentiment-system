from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource
from .dto import tokenization_model
from src.app.core.sentiment_analyse.tokenize_text import (
	process_text_tokenization
)
from ..utilities import utils

ns = Namespace(
	name='Tokenization Controller',
	description='Токенизация текста',
	path='/tokenization/',
	validate=True
)


@ns.route('/tokenize_text')
class TokenizeTextAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Токены текста')
	@ns.expect(tokenization_model)
	@ns.doc(
		description=
		'Разбиение текста на токены с использованием доступных токенизаторов. '
		'Можно добавить стоп-слова и/или использовать пресет по-умолчанию.'
	)
	def post(self):
		""" Токенизация текста """

		# Fill payload with default data
		utils.fill_with_default_values(ns.payload, tokenization_model)
		d = ns.payload

		# Parse payload to get data
		text = d.get('text')
		use_default_stop_words = d.get('useDefaultStopWords')
		stop_words = d.get('stopWords')
		tokenizer_type = d.get('tokenizerType')

		# get tokens with used stop words
		tokens, used_stop_words = process_text_tokenization(
			tokenizer_type,
			text,
			stop_words=stop_words,
			use_default_stop_words=use_default_stop_words
		)

		# return tokens with used stop words
		response = jsonify({
			'tokens': tokens,
			'usedStopWords': list(used_stop_words)
		})
		response.status_code = HTTPStatus.OK

		return response
