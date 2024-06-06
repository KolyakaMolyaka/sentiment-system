import os.path
from http import HTTPStatus
from flask import jsonify, send_file
from flask_restx import Resource, Namespace
from celery.result import AsyncResult

ns = Namespace(
	name='Get Dataset Result Controller',
	description='Получение датасета',
	path='/get_result/',
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
	@ns.response(int(HTTPStatus.BAD_REQUEST), 'Неправильный запрос')
	@ns.doc(
		description='Получение результата запроса по созданию датасета по ID.'
	)
	def get(self, result_id: str):
		"""Получение статуса/результата запроса создания датасета с сайта wildberries"""

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
		if not result.ready():
			response = jsonify({
				# "successful": result.successful(),
				# "value": result.result if result.ready() else None,
				"message": 'Создание датасета находится в обработке.',
			})
			response.status_code = HTTPStatus.OK
			return response

		###### Отправка архива, если датасет готов #### #### ######

		response = jsonify({
				# "successful": result.successful(),
				# "value": result.result if result.ready() else None,
				"feedbacks": result.result[:10],
			})
		response.status_code = HTTPStatus.OK
		return response



		import tempfile
		import json
		import shutil
		feedbacks = result.result

		# Создаем временный файл для сохранения JSON данных словаря
		# with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as temp_file:
		filename = os.path.join(os.path.curdir[:-2], 'dataset.json')
		with open(filename, 'w', encoding='utf-8') as temp_file:
			json.dump(feedbacks, temp_file,
					  ensure_ascii=False)  # Указываем ensure_ascii=False для сохранения кириллических символов корректно


			# Удаляем данные из БД Redis
			# result.forget()

			# Отправляем файл пользователю
			# filename = os.path.join(tempfile.gettempdir(), temp_file.name)
		print(filename)
		return send_file(filename, mimetype='application/json', as_attachment=True, download_name='dataset.json')


