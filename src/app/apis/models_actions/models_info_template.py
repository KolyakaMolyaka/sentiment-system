from abc import ABC, abstractmethod
from src.app.ext.database.models import Tokenizer, Vectorization


class ModelsListInfoTemplate(ABC):

	def __init__(self, db_model):
		self.db_model = db_model

	@abstractmethod
	def get_info(self) -> dict:
		pass

	def _get_general_info(self):
		return {
			'model_title': self.db_model.model_title
		}


class SelfTrainedModelInfo(ModelsListInfoTemplate):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def get_info(self):
		general_info = self._get_general_info()
		model_info = {
			'model_accuracy': self.db_model.model_accuracy,
			'model_precision': self.db_model.model_precision,
			'model_recall': self.db_model.model_recall,
			'trained_self': self.db_model.trained_self,
		}
		return {**model_info, **general_info}


class AlgorithmTrainedModelInfo(ModelsListInfoTemplate):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	def get_info(self):
		general_info = self._get_general_info()

		db_tokenizer = Tokenizer.get_by_id(self.db_model.tokenizer_id)
		db_vectorization = Vectorization.get_by_id(self.db_model.vectorization_id)

		if db_vectorization.title == 'bag-of-words':
			max_words = {'model_max_words': self.db_model.max_words}
		else:
			max_words = {}

		model_info = {
			'model_tokenizer_type': db_tokenizer.title,
			'model_vectorization_type': db_vectorization.title,
			'model_use_default_stop_words': self.db_model.use_default_stop_words,
			'model_accuracy': self.db_model.model_accuracy,
			'model_precision': self.db_model.model_precision,
			'model_recall': self.db_model.model_recall,
			'model_min_token_length': self.db_model.min_token_len,
			'model_delete_numbers_flag': self.db_model.delete_numbers_flag,
		}

		return {**general_info, **model_info, **max_words}
