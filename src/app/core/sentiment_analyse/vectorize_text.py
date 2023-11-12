from collections import Counter


def text_to_sequence(txt: list[str], word_to_index: dict):
	"""
	Преобразование текста в последовательности кодов
	@param: txt:list[str] Список токенов, который необходимо преобразовать в последовательность кодов слов
	@param: word_to_index:dict Словарь, сопоставляющий слово с кодом в последовательности
	"""
	seq = []  # список, содержащий коды слов
	for word in txt:  # получение слова из текста
		index = word_to_index.get(word, 1)  # 1 означает неизвестное слово
		# неизвестные слова не добавляем в выходную последовательность
		if index != 1:
			seq.append(index)
	return seq


def process_convert_tokens_in_seq_of_codes(tokens: list[str], max_words: int = -1):

	if max_words == -1:
		max_words = len(tokens) + 2 # +2 for unknown word and filler

	words = Counter()
	for t in tokens:
		words.update([t])

	# словарь, отображающий слова в коды
	word_to_index = {}
	# словарь, отображающий коды в слова
	index_to_word = {}

	# создание словарей
	for ind, word_tuple in enumerate(words.most_common(max_words - 2)):
		word = word_tuple[0]
		word_to_index[word] = ind + 2
		index_to_word[ind + 2] = word

	seq = text_to_sequence(tokens, word_to_index)
	return seq, word_to_index, index_to_word
