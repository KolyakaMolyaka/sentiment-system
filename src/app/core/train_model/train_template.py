from abc import ABC, abstractmethod

from src.app.core.sentiment_analyse.tokenize_text import process_text_tokenization

from src.app.core.sentiment_analyse.vectorize_text import process_convert_tokens_in_seq_of_codes

from src.app.core.sentiment_analyse.vectorize_text import vectorize_text

class TrainTemplate(ABC):

	def preprocess_text(self, df, tokenizer_type, stop_words, use_default_stop_words):
		""" Токенизация текста """

		# Токенизация текста
		df['preprocessed'] = df.apply(
			lambda row: process_text_tokenization(tokenizer_type, row['text'],
												  stop_words=stop_words,
												  use_default_stop_words=use_default_stop_words)[0],
			axis=1  # axis=1 means row
		)

	@abstractmethod
	def create_sequences(self, df, max_words):
		pass


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


class TrainEmbeddingsAlgorithm(TrainTemplate):
	def create_sequences(self, df, max_words):

		df['sequences'] = df.apply(lambda row:
								   vectorize_text(row['preprocessed'], 100)
								   , axis=1)
		pass
