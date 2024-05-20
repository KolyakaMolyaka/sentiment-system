import numpy
from sklearn.metrics import confusion_matrix, accuracy_score, precision_score, recall_score


def process_user_get_model_metrics(y_true: [str], y_pred: [str], positive_label: str) -> dict:
	"""
	Получение пользователем метрик качества модели МО: confusion matrix, accuracy, precision, recall
	@param y_true: эталонные метки.
	@param y_pred: предсказанные метки.
	@param positive_label: метка класса Positive.
	@return: словарь с необходимыми метриками и их значениями
	"""
	metrics = {}

	metrics['confusion_matrix'] = numpy.flip(confusion_matrix(y_true, y_pred)).tolist()
	metrics['accuracy'] = accuracy_score(y_true, y_pred)
	metrics['precision'] = precision_score(y_true, y_pred, pos_label=positive_label)
	metrics['recall'] = recall_score(y_true, y_pred, pos_label=positive_label)

	return metrics
