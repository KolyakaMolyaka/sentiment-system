from http import HTTPStatus
from flask import abort
from sklearn.linear_model import LogisticRegression
class ClassifierFactory:
	@staticmethod
	def get_classifier(classifier_type, random_state, max_iter):
		""" Получение классификатора """
		classifier = None

		if classifier_type == 'logistic-regression':
			classifier = LogisticRegression(random_state=random_state, max_iter=max_iter)
		else:
			abort(int(HTTPStatus.CONFLICT), 'Неизвестное значение параметра classifier')

		return classifier


