from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource
from .dto import tokenization_model, tokenizer_info_model
from src.app.core.sentiment_analyse.tokenize_text import (
	process_text_tokenization, process_tokenizer_info
)
from ..utilities import utils

ns = Namespace(
	name='Tokenization Controller',
	description='Токенизация текста',
	path='/tokenization/',
	validate=True
)


@ns.route('/tokenizer_info')
class TokenizerInfoAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Информация о токенизаторе')
	@ns.response(int(HTTPStatus.NOT_FOUND), 'Токенизатор не существует')
	@ns.expect(tokenizer_info_model)
	@ns.doc(description='Получение информации о токенизаторе')
	def post(self):
		""" Получение информации о конкретном токенизаторе """
		d = ns.payload

		tokenizer_title = d.get('tokenizerTitle')

		tokenizer_description = process_tokenizer_info(tokenizer_title)

		response = jsonify({
			'tokenizer_title': tokenizer_title,
			'description': tokenizer_description
		})
		response.status_code = HTTPStatus.OK

		return response

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
		min_token_len = d.get('minTokenLength')
		delete_numbers_flag = d.get('deleteNumbers')

		# get tokens with used stop words
		tokens, used_stop_words = process_text_tokenization(
			tokenizer_type,
			text,
			stop_words=stop_words,
			use_default_stop_words=use_default_stop_words,
			min_token_len=min_token_len,
			delete_numbers_flag=delete_numbers_flag
		)

		# return tokens with used stop words
		response = jsonify({
			'tokens': tokens,
			'usedStopWords': list(used_stop_words)
		})
		response.status_code = HTTPStatus.OK

		return response
