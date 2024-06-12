from http import HTTPStatus
from flask import jsonify, abort
from flask_restx import Resource, Namespace
from src.app.core.train_model.train_model_logic import train_model_logic, process_train_model_with_vectors_logic
import pandas as pd

from .dto import train_model, train_model_v2
from src.app.core.auth.auth_logic import requires_auth

ns = Namespace(
	name='Model Train Controller',
	description='Обучение собственных моделей различными способами',
	path='/model_train/',
	validate=True
)


@ns.route('/train_with_teacher/v1')
class ModelTrainWithTeacherAPIv1(Resource):
	method_decorators = [requires_auth]

	@ns.response(int(HTTPStatus.BAD_REQUEST), 'Не совпадает число комментариев с числом классов.')
	@ns.response(int(HTTPStatus.CONFLICT), 'Набор данных имеет длину меньше 2.')
	@ns.response(int(HTTPStatus.NOT_FOUND), 'Указанный токенизатор / метод векторизации / классификатор не существует.')
	@ns.expect(train_model)
	@ns.doc(
		security='basicAuth',
		description='Обучение модели с учителем. '
					'Необходимо указать название создаваемой модели, тип токенизатора, метода векторизации и классификатора. '
					'Ввести знаки препинания (punctuations), минимальную длину токенов (minTokenLength), '
					'стоп-слова (stopWords), указать, нужно ли использовать стоп-слова по умолчанию '
					'(useDefaultStopWords), список исключенных стоп-слов (excludeDefaultStopWords). '
					'Предоставить размеченный набор данных (comments, classes).  '
					'Указать флаг принудительного удаления чисел из токенов (deleteNumbers),  а также максимальное '
					'количество анализируемых слов (maxWords, для обучения алгоритмом "Мешок слов").'
	)
	def post(self):
		""" Обучение модели МО с учителем согласно заданным параметрам """

		MIN_SAMPLE_LEN = 2

		from ..utilities import utils
		utils.fill_with_default_values(ns.payload, train_model)
		d = ns.payload

		# данные для сохранения модели
		model_title = d.get('modelTitle')

		# данные для токенизации
		tokenizer_type = d.get('tokenizerType')
		stop_words = d.get('stopWords')
		use_default_stop_words = d.get('useDefaultStopWords')

		# данные для векторизации
		vectorization_type = d.get('vectorizationType')

		if vectorization_type == 'bag-of-words':
			# проверка, что есть
			# maxWords
			# showUnknownWordCodeInVectors
			pass

		# данные для классификатора
		classifier = d.get('classifier')

		comments = d.get('comments')
		classes = d.get('classes')

		max_words = d.get('maxWords')
		min_token_len = d.get('minTokenLength')
		delete_numbers_flag = d.get('deleteNumbers')
		excluded_default_stop_words = d.get('excludeDefaultStopWords')
		punctuations = d.get('punctuations')

		if len(comments) < MIN_SAMPLE_LEN:
			abort(int(HTTPStatus.CONFLICT), f'Список comments должна иметь длину не меньше {MIN_SAMPLE_LEN}.')
		elif len(classes) < MIN_SAMPLE_LEN:
			abort(int(HTTPStatus.CONFLICT), f'Список classes должна иметь длину не меньше {MIN_SAMPLE_LEN}.')

		if len(comments) != len(classes):
			response = jsonify({
				'error': 'Число комментариев не совпадает с числом классов.'
			})
			response.status_code = HTTPStatus.BAD_REQUEST
			return response

		for c in classes:
			if c not in (0, 1):
				response = jsonify({
					'error': 'Классы могут быть только 0 - отрицательный, 1 - положительный.'
				})
				response.status_code = HTTPStatus.BAD_REQUEST
				return response

		train_info = list(zip(comments, classes))
		df = pd.DataFrame(train_info, columns=['text', 'score'])
		trained_meta = train_model_logic(df, tokenizer_type, stop_words, use_default_stop_words,
										 vectorization_type, model_title, classifier,
										 max_words, classes, comments, min_token_len,
										 delete_numbers_flag, excluded_default_stop_words, punctuations)
		response = jsonify({
			**trained_meta
		})
		response.status_code = HTTPStatus.OK

		return response


@ns.route('/train_with_teacher/v2')
class ModelTrainWithTeacherAPIv2(Resource):
	method_decorators = [requires_auth]

	@ns.response(int(HTTPStatus.BAD_REQUEST), 'Размерность векторов не единого размера.')
	@ns.response(int(HTTPStatus.CONFLICT), 'Длина набора данных меньше 2 или не совпадает (vectors != classes).')
	@ns.expect(train_model_v2)
	@ns.doc(
		desctiption='Обучение модели с помощью полученных пользователем векторных представлений.'
	)
	@ns.doc(security='basicAuth')
	def post(self):
		""" Обучение модели с помощью меток и готовых векторных представлений """

		MIN_TRAIN_SAMPLE_LEN = 2
		d = ns.payload

		model_title = d.get('modelTitle')
		classifier = d.get('classifier')
		vectors = d.get('vectors')
		classes = d.get('classes')

		vectors_len = len(vectors)
		classes_len = len(classes)
		if vectors_len < MIN_TRAIN_SAMPLE_LEN:
			abort(int(HTTPStatus.CONFLICT), f'Длина набора данных должна быть не меньше {MIN_TRAIN_SAMPLE_LEN}! '
											f'vectors не соблюдает это условие.')
		elif classes_len < MIN_TRAIN_SAMPLE_LEN:
			abort(int(HTTPStatus.CONFLICT), f'Длина набора данных должна быть не меньше {MIN_TRAIN_SAMPLE_LEN}! '
											f'classes не соблюдает это условие.')
		elif vectors_len != classes_len:
			abort(int(HTTPStatus.CONFLICT), 'Длина набора данных различается: vectors и classes не совпадают!')

		metrics = process_train_model_with_vectors_logic(model_title, classifier, vectors, classes)

		response = jsonify({
			'статус': f'модель обучена и сохранена под названием {model_title}',
			'metrics': metrics
		})
		response.status_code = HTTPStatus.OK
		return response
