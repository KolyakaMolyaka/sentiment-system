from http import HTTPStatus
from flask import abort
from .tokenizer import NLTKTokenizer, DefaultWhitespaceTokenizer, NLTKWordpunctTokenizer


class TokenizerFactory:
	@staticmethod
	def get_tokenizer(tokenizer_type):
		tokenizer = None

		if tokenizer_type == 'nltk-tokenizer':
			tokenizer = NLTKTokenizer()
		elif tokenizer_type == 'default-whitespace-tokenizer':
			tokenizer = DefaultWhitespaceTokenizer()
		elif tokenizer_type == 'wordpunct-tokenizer':
			tokenizer = NLTKWordpunctTokenizer()
		else:
			abort(int(HTTPStatus.CONFLICT), 'Неизвестный тип токенизатора')

		return tokenizer
