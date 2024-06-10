from http import HTTPStatus
from flask import abort
from sklearn.linear_model import LogisticRegression
class ClassifierFactory:
	@staticmethod
	def get_classifier(classifier_type, random_state=42, max_iter=500):
		""" Получение классификатора """
		classifier = None

		if classifier_type == 'logistic-regression':
			classifier = LogisticRegression(random_state=random_state, max_iter=max_iter)
		else:
			abort(int(HTTPStatus.NOT_FOUND), 'Неизвестное значение параметра classifier')

		return classifier


