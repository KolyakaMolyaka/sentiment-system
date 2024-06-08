from abc import ABC, abstractmethod
from sklearn.model_selection import train_test_split
import numpy as np
from flask import abort
from http import HTTPStatus
from sklearn.linear_model import LogisticRegression
import numpy as np

from src.app.core.sentiment_analyse.tokenize_text import process_text_tokenization

from src.app.core.sentiment_analyse.vectorize_text import process_convert_tokens_in_seq_of_codes

from src.app.core.sentiment_analyse.vectorize_text import vectorize_text, vectorize_sequences


class TrainTemplate(ABC):

	@classmethod
	def get_trained_model_with_samples(cls, train_alg, df, tokenizer_type, stop_words, use_default_stop_words,
									   max_words, classifier, min_token_len, delete_numbers_flag,
									   excluded_default_stop_words):
		""" Шаги выполнения алгоритма с train_alg: TrainTemplate """

		# Препроцессинг текста
		train_alg.preprocess_text(df, tokenizer_type, stop_words, use_default_stop_words, min_token_len,
								  delete_numbers_flag, excluded_default_stop_words)
		# Создание последовательности / векторов
		result = train_alg.create_sequences(df, max_words)
		if result:
			word_to_index, index_to_word = result
		else:
			word_to_index, index_to_word = None, None

		# Получение обучающей и тестовой выборок
		x_train, y_train, x_test, y_test = train_alg.create_train_and_test_samples(df, max_words)

		# Обучение модели
		trained_model = train_alg.train(classifier, x_train, y_train)

		return trained_model, x_train, y_train, x_test, y_test, word_to_index, index_to_word

	def preprocess_text(self, df, tokenizer_type, stop_words, use_default_stop_words, min_token_len,
						delete_numbers_flag, excluded_default_stop_words):
		""" Токенизация текста """

		# Токенизация текста
		df['preprocessed'] = df.apply(
			lambda row: process_text_tokenization(tokenizer_type, row['text'],
												  stop_words=stop_words,
												  use_default_stop_words=use_default_stop_words,
												  min_token_len=min_token_len,
												  delete_numbers_flag=delete_numbers_flag,
												  excluded_default_stop_words=excluded_default_stop_words
												  )[0],
			axis=1  # axis=1 means row
		)

	@abstractmethod
	def create_sequences(self, df, max_words):
		pass

	def train_test_split(self, df, test_size=.2):
		# Получение обучающей и тестовой выборок 80/20 %
		train, test = train_test_split(df, test_size=.2)
		return train, test

	@abstractmethod
	def create_train_and_test_samples(self, df):
		pass

	def train(self, classifier, x_train, y_train, random_state=42, max_iter=500):
		if classifier == 'logistic-regression':
			lr = LogisticRegression(random_state=random_state, max_iter=max_iter)
			lr.fit(x_train, y_train)
			return lr
		else:
			abort(int(HTTPStatus.CONFLICT), 'Неизвестное значение параметра classifier')


class TrainBagOfWordAlgorithm(TrainTemplate):
	def create_sequences(self, df, max_words):
		tokens = []
		for row in df['preprocessed'].tolist():
			tokens.extend(row)

		seq, word_to_index, index_to_word = process_convert_tokens_in_seq_of_codes(tokens, max_words)
		df['sequences'] = df.apply(lambda row:
								   [word_to_index.get(word, 0) for word in row['preprocessed']]
								   , axis=1)
		print('SEQUENCES')
		print(df['sequences'][:4])
		print('END SEQUENCES')

		return [word_to_index, index_to_word]

	def create_train_and_test_samples(self, df, max_words):
		train, test = self.train_test_split(df)
		y_train, y_test = train['score'], test['score']
		x_train = vectorize_sequences(train['sequences'], max_words)
		x_test = vectorize_sequences(test['sequences'], max_words)
		df['vectors'] = df.apply(lambda row: vectorize_sequences([row['sequences']], max_words)[0], axis=1)
		return x_train, y_train, x_test, y_test


class TrainEmbeddingsAlgorithm(TrainTemplate):
	def create_sequences(self, df, max_words):
		df['sequences'] = df.apply(lambda row:
								   vectorize_text(row['preprocessed'], 100)
								   , axis=1)

	def create_train_and_test_samples(self, df, max_words):
		train, test = self.train_test_split(df)
		y_train, y_test = train['score'], test['score']
		x_train = np.array(train['sequences'].tolist()).reshape(len(train), 300 * 100)
		x_test = np.array(test['sequences'].tolist()).reshape(len(test), 300 * 100)
		return x_train, y_train, x_test, y_test
