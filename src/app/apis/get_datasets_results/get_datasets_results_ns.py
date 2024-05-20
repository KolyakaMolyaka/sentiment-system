from http import HTTPStatus
from flask import jsonify
from flask_restx import Resource, Namespace
from celery.result import AsyncResult

ns = Namespace(
	name='Get Dataset Result Controller',
	description='Получение датасета',
	path='/get_result/',
	validate=True
)


@ns.route('/sportmaster/<string:result_id>')
class GetSportmasterDataset(Resource):
	@ns.response(int(HTTPStatus.OK), 'Результат обработки запроса с заданным ID')
	@ns.response(int(HTTPStatus.BAD_REQUEST), 'Неправильный каталог (URL)')
	@ns.doc(
		description='Получение результата запроса по созданию датасета по ID.'
	)
	def get(self, result_id: str):
		"""Получение статуса/результата запроса создания датасета с сайта sportmaster"""

		result = AsyncResult(result_id)

		# Handle failure state
		if result.state == 'FAILURE':
			response = jsonify({
				'successful': result.successful(),
				'msg': 'Проверьте правильность URL'
			})

			response.status_code = HTTPStatus.BAD_REQUEST
			return response

		# Handle successful state
		response = jsonify({
			"successful": result.successful(),
			"value": result.result if result.ready() else None,
		})
		response.status_code = HTTPStatus.OK

		# Forget the result of this task
		result.forget()

		return response
