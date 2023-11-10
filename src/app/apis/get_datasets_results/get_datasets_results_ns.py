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
	@ns.response(int(HTTPStatus.OK), 'Result of task')
	@ns.response(int(HTTPStatus.BAD_REQUEST), 'Invalid catalog url')
	def get(self, result_id: str):
		"""Get status or/and result of sportmaster dataset"""

		result = AsyncResult(result_id)

		# Handle failure state
		if result.state == 'FAILURE':
			response = jsonify({
				'successful': result.successful(),
				'msg': 'check catalog url'
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
