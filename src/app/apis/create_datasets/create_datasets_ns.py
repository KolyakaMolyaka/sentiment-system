from http import HTTPStatus
from flask import jsonify
from flask_restx import Namespace, Resource

from .dto import sportmaster_parser_info_reqparser

ns = Namespace(
	name='Create Dataset Controller',
	description='Создание датасета',
	path='/create_dataset/',
	validate=True
)

from src.app.core.create_datasets.create_datasets_logic import add_together
from celery.result import AsyncResult


@ns.route('/add')
class TestPostAPI(Resource):

	def post(self):
		# a = request.form.get("a", type=int)
		# b = request.form.get("b", type=int)
		a, b = 10, 20
		result = add_together.delay(a, b)
		return {"result_id": result.id}


@ns.route('/result/<id>')
class TestGetAPI(Resource):
	def get(id: str) -> dict[str, object]:
		result = AsyncResult(id)
		return {
			"ready": result.ready(),
			"successful": result.successful(),
			"value": result.result if result.ready() else None,
		}


@ns.route('/sportmaster')
class CreateSportmasterDataset(Resource):
	# @ns.response(int(HTTPStatus.OK))
	@ns.expect(sportmaster_parser_info_reqparser)
	def post(self):
		"""Создание задачи получения датасета"""

		request_body = sportmaster_parser_info_reqparser.parse_args()
		catalog_url: str = request_body.get('catalog_url')
		pages: int = request_body.get('pages')

		# бизнес-логика

		# возврат

		return request_body
