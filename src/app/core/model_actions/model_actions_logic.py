import os
import pickle
import csv
import json
from src.app.ext.database.models import MlModel, User, Vectorization, Tokenizer
from flask import request, abort, current_app
from http import HTTPStatus
from src.app.core.sentiment_analyse.vectorize_text import process_convert_tokens_in_seq_of_codes, vectorize_sequences, text_to_sequence
from src.app.core.sentiment_analyse.tokenize_text import process_text_tokenization
from src.app.core.sentiment_analyse.vectorize_text import vectorize_text
import numpy as np


def load_model(model_title):
	# Загрузка модели (из файла), которую обучал пользователь
	db_user = User.query.filter_by(username=request.authorization.username).one_or_none()
	filename = os.path.join(current_app.config['TRAINED_MODELS'], db_user.username, model_title, 'model.pkl')
	with open(filename, 'rb') as f:
		ml_model = pickle.load(f)
		return ml_model


def load_stop_words(model_title):
	# Загрузка стоп-слов, которые использовал пользователь при обучении модели
	db_user = User.query.filter_by(username=request.authorization.username).one_or_none()
	filename = os.path.join(current_app.config['TRAINED_MODELS'], db_user.username, model_title, 'stop_words.csv')
	stop_words = []
	with open(filename) as csvfile:
		csvreader = csv.reader(csvfile, delimiter=';')
		for row in csvreader:  # формат следующий: ['row']
			stop_words.extend(row)

	return stop_words


def process_model_delete_request(model_title):
	user = User.query.filter_by(username=request.authorization.username).one_or_none()
	model = MlModel.query.filter_by(model_title=model_title, user_id=user.id).one_or_none()
	if not model:
		abort(int(HTTPStatus.NOT_FOUND), f'модель {model_title} не найдена')

	# delete model from db
	MlModel.delete_model(model_title)
	# delete model folder
	import shutil
	username = request.authorization.username
	directory = os.path.join(current_app.config['TRAINED_MODELS'], username, model_title)
	shutil.rmtree(directory)


def process_model_prediction_request(model_title, text, proba=True):
	# Используемые сущности из БД
	db_user = User.query.filter_by(username=request.authorization.username).one_or_none()
	db_model = MlModel.query.filter_by(model_title=model_title, user_id=db_user.id).one_or_none()
	db_vectorization = Vectorization.get_by_id(db_model.vectorization_id)
	db_tokenizer = Tokenizer.get_by_id(db_model.tokenizer_id)

	if not db_model:
		abort(int(HTTPStatus.NOT_FOUND), f'Модель {model_title} не существует.')

	if db_model.trained_self:
		abort(int(HTTPStatus.CONFLICT), f'Модель {model_title} обучалась с уже готовыми векторными представлениями. '
										f'Воспользуйтесь соответствующим контроллером.')

	# Загрузка модели, которую обучал пользователь
	ml_model = load_model(model_title)

	# Загрузка стоп-слов, которые использовал пользователь при обучении модели
	stop_words = load_stop_words(model_title)

	# Выбор алгоритма векторизации, который использовал пользователь при обучении модели
	if db_vectorization.title == 'embeddings':
		preprocessed, stop_words = process_text_tokenization(db_tokenizer.title, text,
															 stop_words=stop_words,
															 use_default_stop_words=db_model.use_default_stop_words)
		vectorized = vectorize_text(preprocessed, 100)
		vector = np.array(vectorized).reshape(1, 300 * 100)

		if proba:
			return ml_model.predict_proba(vector)
		return ml_model.predict(vector)
	elif db_vectorization.title == 'bag-of-words':

		# TEXT TOKENIZATION | STOP WORDS
		preprocessed, stop_words = process_text_tokenization(db_tokenizer.title, text,
															 stop_words=stop_words,
															 use_default_stop_words=db_model.use_default_stop_words)


		word_to_index_filename = os.path.join(current_app.config['TRAINED_MODELS'], db_user.username, model_title, 'word_to_index.json')
		with open(word_to_index_filename, 'r', encoding='utf-8') as f:
			word_to_index = json.load(f)

		seq = text_to_sequence(preprocessed, word_to_index)
		# seq, word_to_index, index_to_word = process_convert_tokens_in_seq_of_codes(preprocessed, db_model.max_words)
		bow = vectorize_sequences([seq], db_model.max_words)
		if proba:
			return ml_model.predict_proba(bow)

	else:
		abort(int(HTTPStatus.CONFLICT), 'неизвестный vectorization type')


def process_model_prediction_with_vector_request(model_title: str, vector: list[float], proba=True):
	db_user = User.query.filter_by(username=request.authorization.username).one_or_none()
	db_model = MlModel.query.filter_by(model_title=model_title, user_id=db_user.id).one_or_none()
	if not db_model:
		abort(int(HTTPStatus.NOT_FOUND), f'Модель {model_title} не найдена')

	if not db_model.trained_self:
		abort(int(HTTPStatus.CONFLICT),
			  f'Модель {model_title} обучалась с помощью определенного алгоритма. Воспользуйтесь соответствующим контроллером.')

	ml_model = load_model(model_title)
	print([vector])
	if proba:
		try:
			return ml_model.predict_proba([vector])
		except ValueError as e:
			import re
			numbers = re.findall(r'\d+', str(e))
			given_features, trained_features = numbers
			abort(int(HTTPStatus.CONFLICT), {
				'error': f'Модель обучалась на входных данных с {trained_features} признаками, вы указали - {given_features}!'
			})
