from http import HTTPStatus
from flask import jsonify, send_file
from flask_restx import Namespace, Resource

from .dto import sportmaster_parser_info_reqparser
from src.app.core.create_datasets.create_datasets_logic import process_create_sportmaster_dataset

ns = Namespace(
	name='Create Dataset Controller',
	description='Creating datasets',
	path='/create_dataset/',
	validate=True
)


@ns.route('/sportmaster')
class CreateSportmasterDataset(Resource):
	@ns.response(int(HTTPStatus.OK), 'Task created successfully')
	@ns.expect(sportmaster_parser_info_reqparser)
	@ns.doc(
		description='Here you can create a task to get a dataset. '
				   'You get the result ID, then you can poll the server for the readiness of the result.'
	)
	def post(self):
		"""Create task of getting dataset from sportmaster"""

		request_body = sportmaster_parser_info_reqparser.parse_args()
		catalog_url: str = request_body.get('catalog_url')
		pages: int = request_body.get('pages')
		# cookies: dict = request_body.get('cookies')
		# headers: dict = request_body.get('headers')

		result = process_create_sportmaster_dataset(catalog_url, pages)

		response = jsonify({
			'result_id': result.id,
			'message': 'task created successfully'
		})
		response.status_code = HTTPStatus.OK

		return response
