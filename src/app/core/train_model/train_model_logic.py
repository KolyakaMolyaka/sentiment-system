from celery import shared_task
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.model_selection import train_test_split

from src.app.core.sentiment_analyse.tokenize_text import process_text_tokenization
from src.app.core.sentiment_analyse.vectorize_text import process_convert_tokens_in_seq_of_codes, text_to_sequence, \
	vectorize_sequences


# @shared_task(ignore_result=False)
def train_model_logic(df, max_words):
	max_words = 10000 + 2
	df['preprocessed'] = df.apply(
		lambda row: process_text_tokenization('nltk-tokenizer', row['text'])[0],
		axis=1 # axis=1 means row
	)

	words = Counter()
	for txt in df['preprocessed']:
		words.update(txt)

	# словарь, оображающий слова в коды
	word_to_index = {}
	# словарь, отображающий коды в слова
	index_to_word = {}

	# создание словарей
	for ind, word in enumerate(words.most_common(max_words - 2)):
		word_to_index[word[0]] = ind + 2
		index_to_word[ind + 2] = word[0]

	df['sequences'] = df.apply(lambda row: text_to_sequence(row['preprocessed'], word_to_index), axis=1)

	train, test = train_test_split(df, test_size=.2)

	# данные для обучения
	x_train_seq = train['sequences']
	y_train = train['score']

	# данные для тестирования
	x_test_seq = test['sequences']
	y_test = test['score']

	# создание мешка слов
	x_train = vectorize_sequences(x_train_seq, max_words)
	x_test = vectorize_sequences(x_test_seq, max_words)

	# обучение модели
	lr = LogisticRegression(random_state=42, max_iter=500)
	lr.fit(x_train, y_train)

	# оценка точности модели
	accuracy = lr.score(x_test, y_test)

	# ROC
	lr_probs = lr.predict_proba(x_test)
	# сохраняет вероятность только для положительного исхода
	lr_probs = lr_probs[::, 1]
	try:
		lr_auc = roc_auc_score(y_test, lr_probs)
		# рассчитываем roc-кривую

	except ValueError:
		err = 'not defined'
		lr_auc = err

	fpr, tpr, treshold = roc_curve(y_test, lr_probs)
	roc_auc = auc(fpr, tpr)

	return {
		'x_train': x_train,
		'y_train': list(y_train),
		'accuracy': accuracy,
		'auc': lr_auc,
		'roc_auc': roc_auc
	}

