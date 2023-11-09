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

