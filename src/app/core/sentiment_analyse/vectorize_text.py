from collections import Counter
import numpy as np
from src.app.ext.database.models import Vectorization
from flask import abort
from http import HTTPStatus


def process_vectorization_info(vectorization_title):
	vectorization = Vectorization.get(vectorization_title)
	if not vectorization:
		abort(int(HTTPStatus.NOT_FOUND), f'Метод векторизации {vectorization_title} не существует')

	return vectorization.description


def vectorize_text(txt: list[str], max_review_len: int):
	"""
	Векторизация текста на основе имеющихся токенов
	@param: txt:list[str] Список токенов, подлежащих векторизации
	@param: navec:Navec модель сопоставления слова к вектору
	@param: max_review_len:int максимальная длина вектора
	"""
	from navec import Navec
	navec_filename = 'navec_hudlit_v1_12B_500K_300d_100q.tar'
	navec = Navec.load(navec_filename)

	unk = navec['<unk>']
	text_embeddings = []
	for token in txt:
		embedding = navec.get(token, unk)
		text_embeddings.append(embedding)

	# Дополняем или обрезаем отзывы для фиксированной длины max_review_len
	l = len(text_embeddings)
	if l > max_review_len:
		text_embeddings = text_embeddings[:max_review_len]
	else:
		text_embeddings.extend([navec['<pad>']] * (max_review_len - l))
	return [list(emb) for emb in text_embeddings]


def vectorize_sequences(sequences: list[list[int]], dimension=5000):
	"""
	Преобразование последовательностей в мешок слов
	@param: sequences:list[list[int]] Список последовательностей кодов, который нужно преобразовать в векторы
	@param: dimension:int размерность каждого преобразованного вектора
	"""
	# (кол-во отзывов x максимальное кол-во используемых слов)
	results = np.zeros((len(sequences), dimension), dtype=int)
	for i, seq in enumerate(sequences):
		for index in seq:
			if index < dimension:
				results[i, index] += 1
	# возвращает список списков (для сериализации)
	return [list(int(num) for num in seq) for seq in results]


def text_to_sequence(txt: list[str], word_to_index: dict):
	"""
	Преобразование текста в последовательности кодов
	@param: txt:list[str] Список токенов, который необходимо преобразовать в последовательность кодов слов
	@param: word_to_index:dict Словарь, сопоставляющий слово с кодом в последовательности
	Используются специальные коды:
		0 - код заполнитель для ограничения до фиксированной длины вектора
		1 - код, обозначающий неизвестное слово (при ограничении кол-ва анализируемых слов)
	"""
	seq = []  # список, содержащий коды слов
	for word in txt:  # получение слова из текста
		index = word_to_index.get(word, 1)  # 1 означает неизвестное слово
		# в выходную последовательность попадают коды неизвестных слов, если это необходимо
		# в ином случае, они не попадают в неё
		seq.append(index)
		# if index != 1:
		# 	seq.append(index)
	return seq


def process_embeddings_vectorization(txt: list[str], max_review_len: int):
	embeddings = vectorize_text(txt, max_review_len)
	return embeddings


def process_vectorize_sequences(sequences: list[list[int]], dimension=-1):
	sequences = vectorize_sequences(sequences, dimension)
	return sequences


def process_convert_tokens_in_seq_of_codes(tokens: list[str], max_words: int = -1):
	if max_words == -1:
		max_words = len(tokens) + 2  # +2 for unknown word and filler

	words = Counter()
	for t in tokens:
		words.update([t])


	# код заполнитель
	filler_code_str = 'код заполнитель'
	filler_code = 0

	# код неизвестного слова
	unknown_code_str = 'код неизвестного слова'
	unknown_code = 1

	# словарь, отображающий слова в коды
	word_to_index = { filler_code_str: filler_code, unknown_code_str: unknown_code }

	# словарь, отображающий коды в слова
	index_to_word = { filler_code: filler_code_str, unknown_code: unknown_code_str }

	# создание словарей
	for ind, word_tuple in enumerate(words.most_common(max_words - 2)):
		word = word_tuple[0]
		word_to_index[word] = ind + 2
		index_to_word[ind + 2] = word

	seq = text_to_sequence(tokens, word_to_index)
	return seq, word_to_index, index_to_word
