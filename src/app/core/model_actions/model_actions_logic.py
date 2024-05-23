from src.app.ext.database.models import MlModel, User
from flask import request, abort
from http import HTTPStatus
def process_model_delete_request(model_title):
	user = User.query.filter_by(username=request.authorization.username).one_or_none()
	model = MlModel.query.filter_by(model_title=model_title, user_id=user.id).one_or_none()
	if not model:
		abort(int(HTTPStatus.NOT_FOUND), f'модель {model_title} не найдена')

	# delete model from db
	MlModel.delete_model(model_title)
	# delete model folder
	# check train_model_logic.py for modelsdir_path
	import shutil
	username = request.authorization.username
	dir_path = '/usr/src/app/src/app/core/train_model'
	modelsdir_path = '/models'
	# import os
	# os.path.join('..', 'train_model', 'models', username, model_title)
	directory = dir_path + rf'{modelsdir_path}/{username}/{model_title}/'
	shutil.rmtree(directory)


def process_model_prediction_request(model_title, text, proba=True):
	user = User.query.filter_by(username=request.authorization.username).one_or_none()
	model = MlModel.query.filter_by(model_title=model_title, user_id=user.id).one_or_none()
	if not model:
		abort(int(HTTPStatus.NOT_FOUND), f'модель {model_title} не найдена')

	# load model
	import pickle
	filename = f'/usr/src/app/src/app/core/train_model/models/{user.username}/{model_title}/model.pkl'
	with open(filename, 'rb') as f:
		ml_model = pickle.load(f)

	filename = f'/usr/src/app/src/app/core/train_model/models/{user.username}/{model_title}/stop_words.txt'
	with open(filename, 'r', encoding='utf-8') as f:
		data = f.read()
		stop_words = data.split(' ')

	print('пользовательские стоп-слова', stop_words)


	if model.vectorization_type == 'embeddings':
		from src.app.core.sentiment_analyse.tokenize_text import process_text_tokenization
		from src.app.core.sentiment_analyse.vectorize_text import vectorize_text
		import numpy as np

		# TEXT TOKENIZATION | STOP WORDS
		preprocessed, stop_words = process_text_tokenization(model.tokenizer_type, text,
															 stop_words=stop_words,
								  use_default_stop_words=model.use_default_stop_words)
		vectorized = vectorize_text(preprocessed, 100)
		vector = np.array(vectorized).reshape(1, 300 * 100)


		if proba:
			return ml_model.predict_proba(vector)
		return ml_model.predict(vector)
	elif model.vectorization_type == 'bag-of-words':

		from src.app.core.sentiment_analyse.vectorize_text import process_convert_tokens_in_seq_of_codes, vectorize_sequences
		from src.app.core.sentiment_analyse.tokenize_text import process_text_tokenization
		# TEXT TOKENIZATION | STOP WORDS
		preprocessed, stop_words = process_text_tokenization(model.tokenizer_type, text,
															 stop_words=stop_words,
								  use_default_stop_words=model.use_default_stop_words)
		seq, word_to_index, index_to_word = process_convert_tokens_in_seq_of_codes(preprocessed, model.max_words)
		bow = vectorize_sequences([seq], model.max_words)
		if proba:
			return ml_model.predict_proba(bow)

	else:
		abort(int(HTTPStatus.CONFLICT), 'неизвестный vectorization type')