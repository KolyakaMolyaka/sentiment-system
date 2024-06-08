from flask import abort, request, current_app
from http import HTTPStatus
from celery import shared_task
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import numpy as np

from src.app.core.sentiment_analyse.vectorize_text import text_to_sequence, \
	vectorize_sequences, vectorize_text

from .model_saver import MlModelSaver

from src.app.ext.database.models import MlModel, User

from .train_template import TrainBagOfWordAlgorithm, TrainEmbeddingsAlgorithm


# ПОД ВОПРОСОМ ДЕКОРАТОР
@shared_task(ignore_result=False)
def train_model_logic(df, tokenizer_type, stop_words, use_default_stop_words,
					  vectorization_type, model_title, classifier,
					  max_words, classes, comments):


	# Проверка, что модели с таким же названием нет
	ml_model = MlModel.get(model_title)
	if ml_model:
		abort(int(HTTPStatus.CONFLICT), f'Модель с названием {model_title} уже существует. Сперва удалите её. Или придумайте новое название.')

	word_to_index, index_to_word = None, None # инициализация для последующего сохранения

	if vectorization_type == 'bag-of-words':
		train_alg = TrainBagOfWordAlgorithm()
	elif vectorization_type == 'embeddings':
		train_alg = TrainEmbeddingsAlgorithm()
	else:
		abort(int(HTTPStatus.BAD_REQUEST, 'Неправильный тип векторизации'))

	train_alg.preprocess_text(df, tokenizer_type, stop_words, use_default_stop_words)
	train_alg.create_sequences(df, max_words)

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
		df['vectors'] = df.apply(lambda row: vectorize_sequences([row['sequences']], max_words)[0], axis=1)

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
	# modelsdir_path = '/models'
	# dir_path = os.path.dirname(os.path.realpath(__file__))
	username = request.authorization.username

	save_dir = current_app.config['TRAINED_MODELS']
	MlModelSaver.verify_path(os.path.join(save_dir, username, model_title)) # ОБЯЗАТЕЛЬНО УБЕДИТЬСЯ

	ml_model_saver = MlModelSaver(save_dir, username, model_title)

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

	return {
		'metrics': metrics,
		'test_accuracy': test_accuracy,
		'roc_auc': roc_auc
	}