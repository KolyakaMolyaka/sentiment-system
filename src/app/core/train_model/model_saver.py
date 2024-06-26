import json
import os
import pickle
import nltk
import csv
import yaml
from sklearn.metrics import roc_auc_score, roc_curve, auc
import matplotlib.pyplot as plt
from src.app.core.metrics.model_metrics_logic import process_user_get_model_metrics

from src.app.ext.database.models import MlModel, Tokenizer, Vectorization


class MlModelSaver:
	def __init__(self, save_dir, model_owner_username, model_title):

		self.metrics = None

		self.save_dir = save_dir
		self.model_owner_username = model_owner_username
		self.model_title = model_title

	def save_model(self, model):
		""" Сериализация обученной модели в файл. model for ex. = LogisticRegression """
		MODEL_FILENAME = 'model.pkl'
		filename = os.path.join(self.save_dir, self.model_owner_username, self.model_title, MODEL_FILENAME)
		self.verify_path(filename)
		with open(filename, 'wb') as f:
			pickle.dump(model, f)

		print('Model saved in ', filename)

	@classmethod
	def verify_path(self, path):
		""" Проверка существования пути, если пути нет, то его создание """
		os.makedirs(os.path.dirname(path), exist_ok=True)

	def save_roc_curve(self, model, x_test, y_test):
		""" Cохранение ROC кривой в файл """

		ROC_CURVE_FILENAME = 'roc_curve.jpg'
		probs = model.predict_proba(x_test)
		preds = probs[:, 1]
		fpr, tpr, threshold = roc_curve(y_test, preds)
		roc_auc = auc(fpr, tpr)

		filename = os.path.join(self.save_dir, self.model_owner_username, self.model_title, ROC_CURVE_FILENAME)
		self.verify_path(filename)
		f = plt.figure()
		f.clear()
		plt.title('ROC кривая')
		plt.plot(fpr, tpr, 'b', label='AUC = %0.2f' % roc_auc)
		plt.legend(loc='lower right')
		plt.plot([0, 1], [0, 1], 'r--')
		plt.xlim([0, 1])
		plt.ylim([0, 1])
		plt.ylabel('True Positive оценка')
		plt.xlabel('False Positive оценка')
		plt.savefig(filename)
		f.clear()
		plt.close(f)

		print('ROC curve saved in:', filename)
		return roc_auc

	def save_dataset(self, comments, classes):
		""" Сохранение обучающего датасета в файл """

		DATASET_FILENAME = 'comments_and_classes.csv'
		filename = os.path.join(self.save_dir, self.model_owner_username, self.model_title, DATASET_FILENAME)
		self.verify_path(filename)

		with open(filename, 'w', newline='') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=';')
			for row in zip(comments, classes):
				csvwriter.writerow(row)

	def load_dataset(self):
		""" Получение датасета, сохраненного с помощью Model_saver.save_dataset()"""
		DATASET_FILENAME = 'comments_and_classes.csv'
		filename = os.path.join(self.save_dir, self.model_owner_username, self.model_title, DATASET_FILENAME)

		result_vectors = []
		result_classes = []
		with open(filename, 'r') as csvfile:
			csvreader = csv.reader(csvfile, delimiter=';')
			for row in csvreader:
				vectors, classes = row
				result_vectors.append(
					list(map(float, vectors[1:-1].split(', ')))  # преобразование строки в список из вещ. чисел
				)
				result_classes.extend(
					[int(classes)]  # преобразование строки в код
				)

		return result_vectors, result_classes

	def save_stop_words(self, stop_words, use_default_stop_words):
		""" Сохранение стоп-слов в файл """

		STOP_WORDS_FILENAME = 'stop_words.csv'
		filename = os.path.join(self.save_dir, self.model_owner_username, self.model_title, STOP_WORDS_FILENAME)
		self.verify_path(filename)

		default_stop_words = set()
		if use_default_stop_words:
			default_stop_words = set(nltk.corpus.stopwords.words('russian'))

		stop_words = set(stop_words).union(default_stop_words)

		with open(filename, 'w') as csvfile:
			csvwriter = csv.writer(csvfile, delimiter=';')

			for row in stop_words:
				csvwriter.writerow([row])

		print('Stop words saved in:', filename)

	def save_dataframe(self, df):
		""" Сохранение датафрейма в файл """

		DF_FILENAME = 'handled_data.csv'
		filename = os.path.join(self.save_dir, self.model_owner_username, self.model_title, DF_FILENAME)
		self.verify_path(filename)

		# df.to_excel(filename, index=True)
		df.to_csv(filename, index=True, sep=';')

		print('Dataframe saved in:', filename)

	def save_model_metrics(self, comments, classes):
		""" Сохранение метрик модели в БД """

		# получение метрик модели
		y_true = []
		for c in classes:
			y_true.append('Positive' if c == 1 else 'Negative')

		y_pred = []
		from src.app.core.model_actions.model_actions_logic import process_model_prediction_request
		for comment in comments:
			prediction = process_model_prediction_request(self.model_title, comment)[0]
			negative_accuracy, positive_accuracy = prediction
			if negative_accuracy > positive_accuracy:
				prediction_result = 'Negative'
			else:
				prediction_result = 'Positive'
			y_pred.append(prediction_result)

		metrics: dict = process_user_get_model_metrics(y_true, y_pred, positive_label='Positive')
		self.metrics = metrics

		ml_model = MlModel.get(self.model_title)
		ml_model.model_recall = metrics['recall']
		ml_model.model_accuracy = metrics['accuracy']
		ml_model.model_precision = metrics['precision']
		ml_model.save()

		print('MlModel metrics saved in database!')
		return metrics

	def save_yaml_model_info(self):
		""" Сохранение информации о модели в yaml формате """

		MODEL_INFO_FILENAME = 'model_info.yaml'

		from src.app.ext.database.models import User
		from flask import request

		db_user = User.get(username=request.authorization.username)
		db_model = MlModel.query.filter_by(user_id=db_user.id, model_title=self.model_title).one_or_none()
		db_tokenizer = Tokenizer.get_by_id(db_model.tokenizer_id)
		db_vectorization = Vectorization.get_by_id(db_model.vectorization_id)

		model_info = {
			'model_title': db_model.model_title,
			'metrics': {
				'accuracy': db_model.model_accuracy,
				'precision': db_model.model_precision,
				'recall': db_model.model_recall,
			}
		}
		if not db_model.trained_self:
			model_info['metrics']['confusion_matrix'] = self.metrics['confusion_matrix']
			model_info['tokenization'] = {
				'tokenizer_type': db_tokenizer.title,
				'tokenizer_description': db_tokenizer.description,
				'min_token_length': db_model.min_token_len,
				'delete_numbers_flag': db_model.delete_numbers_flag,
				'used_default_stop_words': db_model.use_default_stop_words
			}
			model_info['vectorization'] = {
				'vectorization_type': db_vectorization.title,
				'vectorization_description': db_vectorization.description,
				'max_words': db_model.max_words,
			}
			model_info['classifier'] = db_model.classifier
			model_info['trained_self'] = db_model.trained_self

		filename = os.path.join(self.save_dir, self.model_owner_username, self.model_title, MODEL_INFO_FILENAME)
		self.verify_path(filename)

		with open(filename, 'w', encoding='utf-8') as outfile:
			yaml.dump(model_info, outfile, default_flow_style=False, allow_unicode=True)

		print('Model info saved in:', MODEL_INFO_FILENAME)


	def save_bag_of_words_dictionaries(self, word_to_index, index_to_word):
		""" Сохранение словарей для преобразований в файл (для алгоритма мешок слов) """

		WORD_TO_INDEX_FILENAME = 'word_to_index.json'
		INDEX_TO_WORD_FILENAME = 'index_to_word.json'

		filename1 = os.path.join(self.save_dir, self.model_owner_username, self.model_title, WORD_TO_INDEX_FILENAME)
		filename2 = os.path.join(self.save_dir, self.model_owner_username, self.model_title, INDEX_TO_WORD_FILENAME)

		for filename, json_data in ((filename1, word_to_index), (filename2, index_to_word)):
			self.verify_path(filename)

			with open(filename, 'w', encoding='utf-8') as f:
				json.dump(json_data, f, ensure_ascii=False, indent=4)

			print('One of dictionaries saved in', filename)

