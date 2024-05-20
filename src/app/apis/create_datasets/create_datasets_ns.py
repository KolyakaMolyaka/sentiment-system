from http import HTTPStatus
from flask import jsonify, send_file
from flask_restx import Namespace, Resource

from .dto import sportmaster_parser_info_reqparser
from src.app.core.create_datasets.create_datasets_logic import process_create_sportmaster_dataset

ns = Namespace(
	name='Create Dataset Controller',
	description='Создание датасета',
	path='/create_dataset/',
	validate=True
)


@ns.route('/sportmaster')
class CreateSportmasterDataset(Resource):
	@ns.response(int(HTTPStatus.OK), 'Задача успешно создана!')
	@ns.expect(sportmaster_parser_info_reqparser)
	@ns.doc(
		description='Создание задачи для получения датасета. '
				   'Вы получите уникальный ID, который будет использован для получения датасета, когда он будет готов.'
	)
	def post(self):
		"""Создание датасета с сайта sportmaster"""

		request_body = sportmaster_parser_info_reqparser.parse_args()
		catalog_url: str = request_body.get('catalog_url')
		pages: int = request_body.get('pages')
		# cookies: dict = request_body.get('cookies')
		# headers: dict = request_body.get('headers')

		result = process_create_sportmaster_dataset(catalog_url, pages)

		response = jsonify({
			'result_id': result.id,
			'message': 'задача успешно создана'
		})
		response.status_code = HTTPStatus.OK

		return response
