from http import HTTPStatus
from flask import jsonify, send_file, send_from_directory
from flask_restx import Resource, Namespace
from celery.result import AsyncResult

import tempfile
import json

ns = Namespace(
	name='Get Dataset Result Controller',
	description='Получение размеченного набора данных',
	path='/get_dataset/',
	validate=True
)

#
# @ns.route('/sportmaster/<string:result_id>')
# class GetSportmasterDataset(Resource):
# 	@ns.response(int(HTTPStatus.OK), 'Результат обработки запроса с заданным ID')
# 	@ns.response(int(HTTPStatus.BAD_REQUEST), 'Неправильный каталог (URL)')
# 	@ns.doc(
# 		description='Получение результата запроса по созданию датасета по ID.'
# 	)
# 	def get(self, result_id: str):
# 		"""Получение статуса/результата запроса создания датасета с сайта sportmaster"""
#
# 		result = AsyncResult(result_id)
#
# 		# Handle failure state
# 		if result.state == 'FAILURE':
# 			response = jsonify({
# 				'successful': result.successful(),
# 				'msg': 'Проверьте правильность URL'
# 			})
#
# 			response.status_code = HTTPStatus.BAD_REQUEST
# 			return response
#
# 		# Handle successful state
# 		response = jsonify({
# 			"successful": result.successful(),
# 			"value": result.result if result.ready() else None,
# 		})
# 		response.status_code = HTTPStatus.OK
#
# 		# Forget the result of this task
# 		result.forget()
#
# 		return response


@ns.route('/wildberries/<string:result_id>')
class GetWildberriesDataset(Resource):
	@ns.response(int(HTTPStatus.OK), 'Результат обработки запроса с заданным ID')
	@ns.response(int(HTTPStatus.CONFLICT), 'Произошла ошибка в системе очереди задач.')
	@ns.doc(
		description='Получение результата запроса создания размеченного набора данных по ранее выданному уникальному ID.'
	)
	def get(self, result_id: str):
		"""Получение статуса / результата запроса создания размеченного набора данных определенной категории с сайта Wildberries"""

		result = AsyncResult(result_id)

		# Handle failure state
		if result.state == 'FAILURE':
			response = jsonify({
				'successful': result.successful(),
				'msg': 'Проверьте правильность запроса'
			})

			response.status_code = HTTPStatus.BAD_REQUEST
			return response

		# Handle successful state
		if not result.ready() and not result.successful():
			response = jsonify({
				"message": 'Датасет ещё не готов или уже был получен.',
			})
			response.status_code = HTTPStatus.OK
			return response

		feedbacks = result.result
		print(f'Got {len(feedbacks)} feedbacks.')

		# Создаем временный файл для сохранения JSON данных словаря
		with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
			json.dump(feedbacks, temp_file, ensure_ascii=False, indent=2)
			result.forget()
			return send_file(temp_file.name, mimetype='application/octet-stream', as_attachment=True, download_name='dataset.json')

