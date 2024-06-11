import nltk
import pymorphy2
from src.app.ext.database.models import Tokenizer
from flask import abort
from http import HTTPStatus
from .tokenizer_factory import TokenizerFactory


def process_get_default_stop_words() -> list:
	return nltk.corpus.stopwords.words('russian')
def process_text_tokenization(tokenizer_type: str, text: str,
							  punctuation_marks=None, stop_words=None,
							  morph=None,
							  use_default_stop_words=True,
							  min_token_len=1,
							  delete_numbers_flag=False,
							  excluded_default_stop_words: list =None,
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

	PUNCTUATION_MARKS = list('!?,.:;-()') + ['..'] + ['...']
	RUSSIAN_DEFAULT_STOP_WORDS = process_get_default_stop_words()

	if not morph:
		morph = pymorphy2.MorphAnalyzer()

	if not punctuation_marks:
		punctuation_marks = PUNCTUATION_MARKS

	if not excluded_default_stop_words:
		excluded_default_stop_words = set()
	else:
		excluded_default_stop_words = set(
			list(map(str.lower, excluded_default_stop_words))
		)

	if use_default_stop_words:
		default_stop_words = set(RUSSIAN_DEFAULT_STOP_WORDS)
	else:
		default_stop_words = set()

	if stop_words:
		stop_words = set(stop_words).union(default_stop_words)
	else:
		stop_words = default_stop_words

	if excluded_default_stop_words:
		stop_words -= excluded_default_stop_words

	text = text.lower()
	tokenizer: Tokenizer = TokenizerFactory.get_tokenizer(tokenizer_type)
	tokens = tokenizer.tokenize(text)

	preprocessed_text = list()
	for t in tokens:
		# удаление знаков пунктуации из токена
		for p in punctuation_marks:
			t = t.replace(p, '')

		# удаление цифр из токена
		if delete_numbers_flag:
			numbers = list('0123456789')
			for n in numbers:
				t = t.replace(n, '')

		# удаление токенов, длина которых меньше заданной
		if not (len(t) > min_token_len): continue

		# приведение токена в нормальную форму
		lemma = morph.parse(t)[0].normal_form

		# удаление токенов, являющихся стоп-словами
		if lemma in stop_words: continue

		preprocessed_text.append(lemma)

	return preprocessed_text, stop_words


def process_tokenizer_info(tokenizer_title):
	tokenizer = Tokenizer.get(tokenizer_title)
	if not tokenizer:
		abort(int(HTTPStatus.NOT_FOUND), f'Токенизатора {tokenizer_title} не существует')

	return tokenizer.description