import nltk
import pymorphy2
from src.app.ext.database.models import Tokenizer
from flask import abort
from http import HTTPStatus


def process_get_default_stop_words() -> list:
	return nltk.corpus.stopwords.words('russian')
def process_text_tokenization(tokenizer_type: str, text: str,
							  punctuation_marks=None, stop_words=None,
							  morph=None,
							  use_default_stop_words=True,
							  min_token_len=1,
							  delete_numbers_flag=False
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

	if use_default_stop_words:
		default_stop_words = set(RUSSIAN_DEFAULT_STOP_WORDS)
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

	preprocessed_text = set()
	for t in tokens:
		if t in punctuation_marks: continue
		if t in stop_words: continue
		if not (len(t) > min_token_len): continue
		if delete_numbers_flag and t.isdigit(): continue

		lemma = morph.parse(t)[0].normal_form
		if lemma not in stop_words:
			preprocessed_text.add(lemma)

	preprocessed_text = list(preprocessed_text) # нормализация данных
	return preprocessed_text, stop_words


def process_tokenizer_info(tokenizer_title):
	tokenizer = Tokenizer.get(tokenizer_title)
	if not tokenizer:
		abort(int(HTTPStatus.NOT_FOUND), f'Токенизатора {tokenizer_title} не существует')

	return tokenizer.description