import nltk
import pymorphy2


def process_text_tokenization(text: str, punctuation_marks=None, stop_words=None, morph: 'MorphAnalyzer' = pymorphy2.MorphAnalyzer()) -> list[str]:
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
	if not punctuation_marks:
		punctuation_marks = list('!?,.:-()') + ['..'] + ['...']
	if not stop_words:
		stop_words = nltk.corpus.stopwords.words('russian')

	text = text.lower()
	tokens = nltk.tokenize.word_tokenize(text)
	preprocessed_text = []
	for t in tokens:
		if t in punctuation_marks: continue
		if t in stop_words: continue

		lemma = morph.parse(t)[0].normal_form
		if lemma not in stop_words:
			preprocessed_text.append(lemma)
	return preprocessed_text
