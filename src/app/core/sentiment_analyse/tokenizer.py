from abc import ABC, abstractmethod
import nltk
class Tokenizer(ABC):
	""" Токенизатор """

	@abstractmethod
	def tokenize(self, text: str):
		""" Токенизация текста, получение токенов"""


class NLTKTokenizer(Tokenizer):
	def tokenize(self, text: str):
		tokens = nltk.tokenize.word_tokenize(text)
		return tokens

class DefaultWhitespaceTokenizer(Tokenizer):
	def tokenize(self, text: str):
		tokens = text.split()
		return tokens

class NLTKWordpunctTokenizer(Tokenizer):
	def tokenize(self, text: str):
		tokens = nltk.tokenize.wordpunct_tokenize(text)
		return tokens
