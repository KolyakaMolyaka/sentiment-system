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


# ПОД ВОПРОСОМ ДЕКОРАТОР
@shared_task(ignore_result=False)
def train_model_logic(df, tokenizer_type, stop_words, use_default_stop_words,
					  vectorization_type, model_title, classifier,
					  max_words, classes, comments):
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
	lr = None

	if classifier == 'logistic-regression':
		lr = LogisticRegression(random_state=42, max_iter=500)
		lr.fit(x_train, y_train)

	else:
		abort(int(HTTPStatus.CONFLICT), 'Неизвестное значение параметра classifier')

	# оценка точности модели
	test_accuracy = lr.score(x_test, y_test)

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


	filename = dir_path + rf'{modelsdir_path}/{username}/{model_title}/roc_curve.jpg'
	os.makedirs(os.path.dirname(filename), exist_ok=True)
	import matplotlib.pyplot as plt
	plt.plot(fpr, tpr)
	plt.ylabel('True Positive Rate')
	plt.xlabel('False Positive Rate')
	plt.savefig(filename)

	filename = dir_path + rf'{modelsdir_path}/{username}/{model_title}/model.pkl'
	os.makedirs(os.path.dirname(filename), exist_ok=True)

	with open(filename, 'wb') as f:
		pickle.dump(lr, f)


	def save_sample_in_file(filename,data, delim='\n\n'):
		with open(filename, 'w', encoding='utf-8') as f:
			vectors = []
			for vector in data:
				str_vector = list(map(str, vector))
				vectors.append(','.join(str_vector))
			f.write(delim.join(vectors))

	# x_train
	filename = dir_path + rf'{modelsdir_path}/{username}/{model_title}/x_train.txt'
	save_sample_in_file(filename, x_train)

	# x_test
	filename = dir_path + rf'{modelsdir_path}/{username}/{model_title}/x_test.txt'
	save_sample_in_file(filename, x_test)

	# y_train
	with open(dir_path + rf'{modelsdir_path}/{username}/{model_title}/y_train.txt', 'w') as f:
		f.write(','.join(list(map(str, list(y_train)))))

	# y_test
	with open(dir_path + rf'{modelsdir_path}/{username}/{model_title}/y_test.txt', 'w') as f:
		f.write(','.join(list(map(str, y_test))))

	with open(dir_path + rf'{modelsdir_path}/{username}/{model_title}/stop_words.txt', 'w', encoding='utf-8') as f:
		f.write(' '.join(stop_words))

	from src.app.ext.database.models import MlModel, User
	user = User.get(request.authorization.username)
	for m in user.ml_models:
		if m.model_title == model_title:
			abort(int(HTTPStatus.CONFLICT), f'Модель с названием {model_title} уже существует. Сперва удалите её.')

	new_model = MlModel(model_title=model_title,
						# model_accuracy=metrics['accuracy'],
						# model_recall=metrics['recall'],
						# model_precision=metrics['precision'],
						classifier=classifier,
						tokenizer_type=tokenizer_type,
						vectorization_type=vectorization_type,
						use_default_stop_words=use_default_stop_words,
						max_words=max_words,
						user_id=user.id)

	new_model.save()


	# получение метрик модели
	y_true = []
	for c in classes:
		y_true.append('Positive' if c == 1 else 'Negative')
	print('y_true', y_true)

	y_pred = []
	from src.app.core.model_actions.model_actions_logic import process_model_prediction_request
	for comment in comments:
		prediction = process_model_prediction_request(model_title, comment)[0]
		negative_accuracy, positive_accuracy = prediction
		if negative_accuracy > positive_accuracy:
			prediction_result = 'Negative'
		else:
			prediction_result = 'Positive'
		y_pred.append(prediction_result)

	print('y_pred', y_pred)

	from src.app.core.metrics.model_metrics_logic import process_user_get_model_metrics
	metrics: dict = process_user_get_model_metrics(y_true, y_pred, positive_label='Positive')

	new_model.model_recall = metrics['recall']
	new_model.model_accuracy = metrics['accuracy']
	new_model.model_precision = metrics['precision']
	new_model.save()

	return {
		# 'x_train': x_train,
		# 'y_train': y_train,
		'metrics': metrics,
		'test_accuracy': test_accuracy,
		'auc': lr_auc,
		'roc_auc': roc_auc
	}