from flask import abort, request
from http import HTTPStatus
from celery import shared_task
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.model_selection import train_test_split
import numpy as np

from src.app.core.sentiment_analyse.tokenize_text import process_text_tokenization
from src.app.core.sentiment_analyse.vectorize_text import process_convert_tokens_in_seq_of_codes, text_to_sequence, \
	vectorize_sequences, vectorize_text

from src.app.core.sentiment_analyse.vectorize_text import process_embeddings_vectorization


@shared_task(ignore_result=False)
def train_model_logic(df, tokenizer_type, stop_words, use_default_stop_words,
					  vectorization_type, model_title,
					  max_words):
	# max_words = 10000 + 2
	df['preprocessed'] = df.apply(
		lambda row: process_text_tokenization(tokenizer_type, row['text'],
											  stop_words=stop_words,
											  use_default_stop_words=use_default_stop_words)[0],
		axis=1 # axis=1 means row

	)

	print('PREPROCESSED')
	print(df['preprocessed'][:4])

	if vectorization_type == 'bag-of-words':
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

	elif vectorization_type == 'embeddings':

		df['sequences'] = df.apply(lambda row:
								   # [
									   # [float(num) for num in vect]
									   # for vect in process_embeddings_vectorization(row['preprocessed'], len(row['preprocessed']))
								   # ]
								   # process_embeddings_vectorization(row['preprocessed'], len(row['preprocessed']))[0]
								   vectorize_text(row['preprocessed'], 100)
								   , axis=1)
		# print("SEQUENCES")
		# print(df['sequences'][:4])
		# print(len(df['sequences'][0]))
		# print(df['sequences'].tolist())
		# for tokens in df['preprocessed'].tolist():
		# 	embeddings = process_embeddings_vectorization()
		# 	embeddings = [[float(num) for num in vect] for vect in embeddings]
		# 	list_of_embeddings.append(embeddings)
		# print(list_of_embeddings)
	else:
		abort(int(HTTPStatus.BAD_REQUEST, 'Неправильный тип векторизации'))

	train, test = train_test_split(df, test_size=.2)

	# данные для обучения
	x_train_seq = train['sequences']
	y_train = train['score']

	# данные для тестирования
	x_test_seq = test['sequences']
	y_test = test['score']

	if vectorization_type == 'bag-of-words':
		# создание мешка слов
		x_train = vectorize_sequences(x_train_seq, max_words)
		x_test = vectorize_sequences(x_test_seq, max_words)
	else:
		x_train = np.array(train['sequences'].tolist()).reshape(len(train), 300 * 100)
		x_test = np.array(test['sequences'].tolist()).reshape(len(test), 300 * 100)

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

	if vectorization_type == 'embeddings':
		x_train = x_train.tolist()
		y_train = y_train.tolist()


	# сохранение модели в папке пользователя
	# данные для тренировки (x, y)
	# данные для проверки (x, y)
	# обученная модель
	# метрики качества

	import pickle
	import os
	dir_path = os.path.dirname(os.path.realpath(__file__))
	# write models
	modelsdir_path = '/models'
	username = request.authorization.username

	filename = dir_path + rf'{modelsdir_path}/{username}/{model_title}/model.pkl'
	os.makedirs(os.path.dirname(filename), exist_ok=True)

	with open(dir_path + rf'{modelsdir_path}/{username}/{model_title}/model.pkl', 'wb') as f:
		pickle.dump(lr, f)

	from src.app.ext.database.models import MlModel, User
	user = User.get(request.authorization.username)
	for m in user.ml_models:
		if m.model_title == model_title:
			abort(int(HTTPStatus.CONFLICT), f'Модель с названием {model_title} уже существует. Сперва удалите её.')
	new_model = MlModel(model_title=model_title, model_accuracy=accuracy,user_id=user.id)
	new_model.save()

	return {
		# 'x_train': x_train,
		# 'y_train': y_train,
		'accuracy': accuracy,
		'auc': lr_auc,
		'roc_auc': roc_auc
	}

