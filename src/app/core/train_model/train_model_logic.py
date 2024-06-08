from flask import abort, request, current_app
from http import HTTPStatus
from celery import shared_task

from .model_saver import MlModelSaver

from src.app.ext.database.models import MlModel, User

from .train_template import TrainBagOfWordAlgorithm, TrainEmbeddingsAlgorithm, TrainTemplate


# ПОД ВОПРОСОМ ДЕКОРАТОР
@shared_task(ignore_result=False)
def train_model_logic(df, tokenizer_type, stop_words, use_default_stop_words,
					  vectorization_type, model_title, classifier,
					  max_words, classes, comments, min_token_len=1,
					  delete_numbers_flag=False, excluded_default_stop_words=None):
	# Проверка, что модели с таким же названием нет
	ml_model = MlModel.get(model_title)
	if ml_model:
		abort(int(HTTPStatus.CONFLICT),
			  f'Модель с названием {model_title} уже существует. Сперва удалите её. Или придумайте новое название.')

	word_to_index, index_to_word = None, None  # инициализация для последующего сохранения

	if vectorization_type == 'bag-of-words':
		train_alg = TrainBagOfWordAlgorithm()
	elif vectorization_type == 'embeddings':
		train_alg = TrainEmbeddingsAlgorithm()
	else:
		abort(int(HTTPStatus.BAD_REQUEST, 'Неправильный тип векторизации'))

	trained_model, \
		x_train, \
		y_train, \
		x_test, \
		y_test = TrainTemplate.get_trained_model_with_samples(train_alg, df, tokenizer_type, stop_words,
															  use_default_stop_words, max_words, classifier,
															  min_token_len, delete_numbers_flag,
															  excluded_default_stop_words)
	# оценка точности модели
	test_accuracy = trained_model.score(x_test, y_test)

	# сохранение модели в папке пользователя
	import os
	username = request.authorization.username

	save_dir = current_app.config['TRAINED_MODELS']
	MlModelSaver.verify_path(os.path.join(save_dir, username, model_title))  # ОБЯЗАТЕЛЬНО УБЕДИТЬСЯ

	ml_model_saver = MlModelSaver(save_dir, username, model_title)

	# Сохранение модели в файл
	ml_model_saver.save_model(trained_model)

	# Сохранение ROC кривой в файл
	roc_auc = ml_model_saver.save_roc_curve(trained_model, x_test, y_test)

	# Сохранение стоп-слов в файл
	ml_model_saver.save_stop_words(stop_words, use_default_stop_words)

	# Сохранение датафрейма в файл
	ml_model_saver.save_dataframe(df)

	if vectorization_type == 'bag-of-words':
		# сохранение преобразования слов в коды
		ml_model_saver.save_bag_of_words_dictionaries(word_to_index, index_to_word)

	def save_sample_in_file(filename, data, delim='\n\n'):
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
