import nltk
import pymorphy2
from src.app.ext.database.models import Tokenizer
from flask import abort
from http import HTTPStatus


def process_text_tokenization(tokenizer_type: str, text: str,
							  punctuation_marks=None, stop_words=None,
							  morph=None,
							  use_default_stop_words=True
							  ) -> tuple[list[str], list[str]]:
	"""
	Вход:
		- текст комментария
		- стоп слова, которые необходимо удалить
		- знаки пунктуации, которые необходимо удалить
		- морфологический анализатор для лемматизации
	Описание функции:
		- приведение текста к нижнему регистру
		- выделение токенов в тексте
		- удаление знаков препинания
		- удаление стоп слов
		- приведение оставшихся токенов к нормальной форме (лемматизация)

	Выход:
		- список с обработанными токенами.
	"""
	if not morph:
		morph = pymorphy2.MorphAnalyzer()

	if not punctuation_marks:
		punctuation_marks = list('!?,.:-()') + ['..'] + ['...']

	if use_default_stop_words:
		default_stop_words = set(nltk.corpus.stopwords.words('russian'))
	else:
		default_stop_words = set()

	if stop_words:
		stop_words = set(stop_words).union(default_stop_words)
	else:
		stop_words = default_stop_words

	text = text.lower()
	if tokenizer_type == 'nltk-tokenizer':
		tokens = nltk.tokenize.word_tokenize(text)
	elif tokenizer_type == 'default-whitespace-tokenizer':
		tokens = text.split()
	elif tokenizer_type == 'wordpunct-tokenizer':
		tokens = nltk.tokenize.wordpunct_tokenize(text)
	else:
		# default nltk-tokenizer
		tokens = nltk.tokenize.word_tokenize(text)

	preprocessed_text = []
	for t in tokens:
		if t in punctuation_marks: continue
		if t in stop_words: continue

		lemma = morph.parse(t)[0].normal_form
		if lemma not in stop_words:
			preprocessed_text.append(lemma)

	return preprocessed_text, stop_words


def process_tokenizer_info(tokenizer_title):
	tokenizer = Tokenizer.get(tokenizer_title)
	if not tokenizer:
		abort(int(HTTPStatus.NOT_FOUND), f'Токенизатора {tokenizer_title} не существует')

	return tokenizer.description