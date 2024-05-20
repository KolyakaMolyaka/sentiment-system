from http import HTTPStatus
from flask import jsonify
from flask_restx import Resource, Namespace
from src.app.core.auth.auth_logic import (
	process_login_from_form,
	process_register_from_form,
	requires_auth
)
from .dto import auth_from_form_reqparser

ns = Namespace(
	name='Auth Controller',
	description='Авторизация',
	path='/auth/',
	validate=True
)


@ns.route('/logout')
class LogoutAPI(Resource):
	method_decorators = [requires_auth]

	@ns.response(int(HTTPStatus.OK), 'Пользователь вышел из аккаунта.')
	@ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь неавторизован.')
	@ns.doc(security='basicAuth')
	def post(self):
		return {'message': 'Вы неавторизованы!'}


# @ns.route('/login')
# class LoginAPI(Resource):
# 	@ns.expect(auth_from_form_reqparser)
# 	def post(self):
# 		form_data = auth_from_form_reqparser.parse_args()
#
# 		process_login_from_form(**form_data)
#
# 		return form_data


@ns.route('/register')
class RegisterAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Пользователь успешно зарегистрирован.')
	@ns.response(int(HTTPStatus.CONFLICT), 'User with the same username is already exists.')
	@ns.expect(auth_from_form_reqparser)
	def post(self):
		"""Регистрация нового пользователя"""
		form_data = auth_from_form_reqparser.parse_args()

		process_register_from_form(**form_data)
		response = jsonify({'message': 'пользователь успешно зарегисрирован'})
		response.status_code = HTTPStatus.OK
		return response
