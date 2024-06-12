from src.app.ext.database.models import User, MlModel
from http import HTTPStatus
from flask import abort, request, current_app

import os
import csv

import numpy
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score
from src.app.core.model_actions.model_actions_logic import process_model_prediction_with_vector_request, \
	process_model_prediction_request
import pandas as pd


def process_user_get_model_metrics(y_true: [str], y_pred: [str], positive_label: str, show_warnings=False) -> dict:
	"""
	Получение пользователем метрик качества модели МО: confusion matrix, accuracy, precision, recall
	@param y_true: эталонные метки.
	@param y_pred: предсказанные метки.
	@param positive_label: метка класса Positive.
	@return: словарь с необходимыми метриками и их значениями
	"""

	# TODO: метрики должны быть и положительными и отрицательным
	if show_warnings:
		if all([1 if y == 'Positive' else 0 for y in y_pred]):
			return {
				'message': 'хотя бы одна предсказанная метрика должна быть '
			}

	metrics = {}

	metrics['confusion_matrix'] = numpy.flip(confusion_matrix(y_true, y_pred)).tolist()
	metrics['accuracy'] = accuracy_score(y_true, y_pred)
	metrics['precision'] = precision_score(y_true, y_pred, pos_label=positive_label)
	metrics['recall'] = recall_score(y_true, y_pred, pos_label=positive_label)

	return metrics


def process_user_calculate_model_metrics(model_title: str, get_from_db_flag: bool, save_in_db_flag: bool = True):
	user = User.get(username=request.authorization.username)
	ml_model = MlModel.query.filter_by(user_id=user.id, model_title=model_title).one_or_none()

	if not ml_model:
		abort(int(HTTPStatus.NOT_FOUND), f'Модель {model_title} не существует.')

	if get_from_db_flag:
		metrics = {
			'accuracy': ml_model.model_accuracy,
			'precision': ml_model.model_precision,
			'recall': ml_model.model_recall
		}
		return metrics
	if ml_model.trained_self:

		DATASET_FILENAME = 'comments_and_classes.csv'
		filename = os.path.join(current_app.config['TRAINED_MODELS'], user.username, model_title, DATASET_FILENAME)
		dataset = []
		classes = []
		with open(filename, 'r') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=';')
			for row in csvreader:
				vectors, class_ = row
				dataset.append(
					list(map(float, vectors[1:-1].split(', '))) # преобразование строки в список из вещ. чисел
				)
				print(classes)
				classes.append(int(class_))
				# classes.extend(
				# 	[int(classes)] # преобразование строки в код
				# )


		# предсказание модели на основе датасета
		y_true = ['Positive' if c == 1 else 'Negative' for c in classes]
		y_pred = []

		for v in dataset:
			prediction = process_model_prediction_with_vector_request(model_title, v)[0]
			negative_accuracy, positive_accuracy = prediction
			if negative_accuracy > positive_accuracy:
				prediction_result = 'Negative'
			else:
				prediction_result = 'Positive'
			y_pred.append(prediction_result)

		metrics: dict = process_user_get_model_metrics(y_true, y_pred, positive_label='Positive')



	else:
		# TODO: расчёт метрик для обычных моделей
		DATASET_FILENAME = 'handled_data.csv'

		filename = os.path.join(current_app.config['TRAINED_MODELS'], user.username, model_title, DATASET_FILENAME)
		df = pd.read_csv(filename, sep=';')

		classes = df['score'].tolist()
		comments = df['text'].tolist()

		y_true = []
		for c in classes:
			y_true.append('Positive' if c == 1 else 'Negative')

		y_pred = []
		for comment in comments:
			prediction = process_model_prediction_request(model_title, comment)[0]
			negative_accuracy, positive_accuracy = prediction
			if negative_accuracy > positive_accuracy:
				prediction_result = 'Negative'
			else:
				prediction_result = 'Positive'
			y_pred.append(prediction_result)

		metrics: dict = process_user_get_model_metrics(y_true, y_pred, positive_label='Positive')
	if save_in_db_flag:
		ml_model.model_recall = metrics['recall']
		ml_model.model_accuracy = metrics['accuracy']
		ml_model.model_precision = metrics['precision']
		ml_model.save()
	return metrics