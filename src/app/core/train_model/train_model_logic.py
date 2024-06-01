from flask import abort, request
from http import HTTPStatus
from celery import shared_task
from collections import Counter
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve, auc
from sklearn.model_selection import train_test_split
import numpy as np

from src.app.core.sentiment_analyse.tokenize_text import process_text_tokenization
from src.app.core.sentiment_analyse.vectorize_text import text_to_sequence, \
	vectorize_sequences, vectorize_text

from .model_saver import MlModelSaver

from src.app.ext.database.models import MlModel, User


# ПОД ВОПРОСОМ ДЕКОРАТОР
@shared_task(ignore_result=False)
def train_model_logic(df, tokenizer_type, stop_words, use_default_stop_words,
					  vectorization_type, model_title, classifier,
					  max_words, classes, comments):


	# user = User.get(request.authorization.username)
	# for m in user.ml_models:
		# if m.model_title == model_title:

	# Проверка, что модели с таким же названием же нет
	ml_model = MlModel.get(model_title)
	if ml_model:
		abort(int(HTTPStatus.CONFLICT), f'Модель с названием {model_title} уже существует. Сперва удалите её.')


	df['preprocessed'] = df.apply(
		lambda row: process_text_tokenization(tokenizer_type, row['text'],
											  stop_words=stop_words,
											  use_default_stop_words=use_default_stop_words)[0],
		axis=1 # axis=1 means row
	)

	print('PREPROCESSED')
	print(df['preprocessed'][:4])

	word_to_index, index_to_word = None, None # инициализация для последующего сохранения

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
								   vectorize_text(row['preprocessed'], 100)
								   , axis=1)
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

	if vectorization_type == 'embeddings':
		x_train = x_train.tolist()
		y_train = y_train.tolist()

	# сохранение модели в папке пользователя

	import os
	modelsdir_path = '/models'
	dir_path = os.path.dirname(os.path.realpath(__file__))
	username = request.authorization.username

	MlModelSaver.verify_path(os.path.join('models', username, model_title)) # ОБЯЗАТЕЛЬНО УБЕДИТЬСЯ
	ml_model_saver = MlModelSaver(dir_path, username, model_title)

	# Сохранение модели в файл
	ml_model_saver.save_model(lr)
	# Сохранение ROC кривой в файл
	roc_auc = ml_model_saver.save_roc_curve(lr, x_test, y_test)
	# Сохранение обучающего датасета
	# ml_model_saver.save_dataset(comments, df['preprocessed'].tolist(), classes)
	# Сохранение обучающих векторов в файл
	# ...
	# Сохранение стоп-слов в файл
	ml_model_saver.save_stop_words(stop_words, use_default_stop_words)
	# Сохранение датафрейма в файл
	ml_model_saver.save_dataframe(df)
	if vectorization_type == 'bag-of-words':
		# сохранение преобразования слов в коды
		ml_model_saver.save_bag_of_words_dictionaries(word_to_index, index_to_word)

	def save_sample_in_file(filename,data, delim='\n\n'):
		os.makedirs(os.path.dirname(filename), exist_ok=True)
		with open(filename, 'w', encoding='utf-8') as f:
			vectors = []
			for vector in data:
				str_vector = list(map(str, vector))
				vectors.append(','.join(str_vector))
			f.write(delim.join(vectors))


	""" *_train, *_test 
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
	"""


	new_model = MlModel(model_title=model_title,
						classifier=classifier,
						tokenizer_type=tokenizer_type,
						vectorization_type=vectorization_type,
						use_default_stop_words=use_default_stop_words,
						max_words=max_words,
						user_id=User.get(username=username).id)

	new_model.save()

	metrics = ml_model_saver.save_model_metrics(comments, classes)

	ml_model_saver.save_yaml_model_info()


	# # получение метрик модели
	# y_true = []
	# for c in classes:
	# 	y_true.append('Positive' if c == 1 else 'Negative')
	#
	# y_pred = []
	# from src.app.core.model_actions.model_actions_logic import process_model_prediction_request
	# for comment in comments:
	# 	prediction = process_model_prediction_request(model_title, comment)[0]
	# 	negative_accuracy, positive_accuracy = prediction
	# 	if negative_accuracy > positive_accuracy:
	# 		prediction_result = 'Negative'
	# 	else:
	# 		prediction_result = 'Positive'
	# 	y_pred.append(prediction_result)
	#
	#
	# from src.app.core.metrics.model_metrics_logic import process_user_get_model_metrics
	# metrics: dict = process_user_get_model_metrics(y_true, y_pred, positive_label='Positive')
	#
	# new_model.model_recall = metrics['recall']
	# new_model.model_accuracy = metrics['accuracy']
	# new_model.model_precision = metrics['precision']
	# new_model.save()

	return {
		'metrics': metrics,
		'test_accuracy': test_accuracy,
		'roc_auc': roc_auc
	}