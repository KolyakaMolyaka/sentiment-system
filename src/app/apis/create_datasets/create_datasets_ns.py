from http import HTTPStatus
from flask import jsonify, send_file, abort
from flask_restx import Namespace, Resource
from src.app.parsers.wb_parser.entities.wbmenu import WbMenu

from .dto import sportmaster_parser_info_reqparser, wildberries_parser_info_reqparser
from src.app.core.create_datasets.create_datasets_logic import process_create_sportmaster_dataset, process_create_wildberries_dataset

ns = Namespace(
	name='Create Dataset Controller',
	description='Создание размеченного набора данных',
	path='/create_dataset/',
	validate=True
)

# @ns.route('/sportmaster')
# class CreateSportmasterDataset(Resource):
# 	@ns.response(int(HTTPStatus.OK), 'Задача успешно создана!')
# 	@ns.expect(sportmaster_parser_info_reqparser)
# 	@ns.doc(
# 		description='Создание задачи для получения датасета. '
# 				   'Вы получите уникальный ID, который будет использован для получения датасета, когда он будет готов.'
# 	)
# 	def post(self):
# 		"""Создание датасета с сайта sportmaster"""
#
# 		request_body = sportmaster_parser_info_reqparser.parse_args()
# 		catalog_url: str = request_body.get('catalog_url')
# 		pages: int = request_body.get('pages')
# 		# cookies: dict = request_body.get('cookies')
# 		# headers: dict = request_body.get('headers')
#
# 		result = process_create_sportmaster_dataset(catalog_url, pages)
#
# 		response = jsonify({
# 			'result_id': result.id,
# 			'message': 'задача успешно создана'
# 		})
# 		response.status_code = HTTPStatus.OK
#
# 		return response

@ns.route('/wildberries_menu')
class CreateWildberriesMenu(Resource):
	@ns.response(int(HTTPStatus.OK), 'Список категорий и подкатегорий.')
	@ns.doc(description='Получение списка категорий и подкатегорий для создания размеченного набора данных.')
	def get(self):
		""" Получение списка категорий и подкатегорий с сайта Wildberries, которые можно использовать для создания размеченного набора данных """

		wb_menu = WbMenu()
		menu = wb_menu.get_menu()
		response = jsonify({
			'menu': menu
		})
		response.status_code = HTTPStatus.OK
		return response


@ns.route('/wildberries')
class CreateWildberriesDataset(Resource):
	@ns.response(int(HTTPStatus.OK), 'Задача успешно создана.')
	@ns.response(int(HTTPStatus.CONFLICT), 'Количество запрашиваемых страниц должно быть больше нуля.')
	@ns.expect(wildberries_parser_info_reqparser)
	@ns.doc(
		description='Создание задачи для получения размеченного набора данных. '
					'Для получения результата набора данных необходимо сохранить выданный уникальный ID. '
					'Получить набор по выданному ID можно только один раз! Создайте новый запрос, если хотите получить '
					'набор данных ещё раз.'
	)
	def post(self):
		"""Создание размеченного набора данных с сайта Wildberries в определенной категории товаров """

		request_body = wildberries_parser_info_reqparser.parse_args()
		category: str = request_body.get('category')
		subcategory: str = request_body.get('subcategory')
		pages: int = request_body.get('pages')

		if pages <= 0:
			abort(int(HTTPStatus.CONFLICT), 'Укажите корректное количество страниц большее нуля')

		result = process_create_wildberries_dataset(category, subcategory, pages)

		response = jsonify({
			'result_id': result.id,
			'message': 'задача успешно создана'
		})
		response.status_code = HTTPStatus.OK

		return response

