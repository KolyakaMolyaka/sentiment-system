import os
import pickle
from flask import abort, current_app
from .tokenize_text import process_text_tokenization
from .vectorize_text import process_convert_tokens_in_seq_of_codes, vectorize_sequences, vectorize_text
import numpy as np

def embeddings_predict(text, model, proba=False):
	max_review_len = 100 # pretrained max words configuration
	vector_size = 300 # pretrainded vector size config
	tokens, _ = process_text_tokenization('nltk-tokenizer', text)
	vectorized = vectorize_text(tokens, max_review_len)
	vector = np.array(vectorized).reshape(1, vector_size*max_review_len)
	if proba:
		return model.predict_proba(vector)
	return model.predict(vector)

def predict(text: str, model, proba=False):
	"""
	Определение тональности по тексту комментария
	@param: text:str Текст комментария для анализа тональности
	@param: proba:bool Нужно ли вернуть массив с вероятностью принадлежностью к классу
	@return: int Класс, которому соответствует тональность комментария
	"""
	max_words = 10000 # pretrained max words configuration
	tokens, _ = process_text_tokenization('nltk-tokenizer', text)
	seq, _, _ = process_convert_tokens_in_seq_of_codes(tokens, max_words)
	X = vectorize_sequences([seq], max_words)
	if proba:
		return model.predict_proba(X)
	return model.predict(X)


def process_analyse_text(model_type: str, text: str):


	if model_type == 'bag-of-words':
		simple_vmp_filename = os.path.join(current_app.config['PRETRAINED_MODELS'],
										   'SIMPLE_VECTORIZATION_PRETRAINED_MODEL.pkl')
		with open(simple_vmp_filename, 'rb') as f:
			simple_vpm = pickle.load(f)

		model = simple_vpm
		prediction = predict(text, model, proba=True)[0]
	elif model_type == 'embeddings':
		embedding_vpm_filename = os.path.join(current_app.config['PRETRAINED_MODELS'],
										   'EMBEDDINGS_PRETRAINED_MODEL.pkl')
		with open(embedding_vpm_filename, 'rb') as f:
			embedding_vpm = pickle.load(f)

		model = embedding_vpm
		prediction = embeddings_predict(text, model, proba=True)[0]

	mapper = np.argmax(prediction)
	sentiment = 'Negative' if mapper == 0 else 'Positive'

	sentiment_description = {
		'sentiment': sentiment,
		# порядок важен, prediction[0] -> negative
		'negativeProbability': prediction[0],
		'positiveProbability': prediction[1]
	}
	return sentiment_description