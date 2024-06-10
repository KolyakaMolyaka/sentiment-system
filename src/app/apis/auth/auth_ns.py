from http import HTTPStatus
from flask import jsonify
from flask_restx import Resource, Namespace
from src.app.core.auth.auth_logic import (
	process_register_from_form,
	requires_auth
)
from .dto import auth_from_form_reqparser

ns = Namespace(
	name='Authorization Controller',
	description='Регистрация / авторизация пользователя в системе',
	path='/auth/',
	validate=True
)


# @ns.route('/check_auth')
# class CheckAuth(Resource):
# 	method_decorators = [requires_auth]
#
# 	@ns.response(int(HTTPStatus.OK), 'Пользователь авторизован')
# 	@ns.response(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не авторизован.')
# 	@ns.doc(security='basicAuth')
# 	def post(self):
# 		"""Проверка авторизации пользователя """
# 		authorized, message = process_user_check_authorization()
# 		response = jsonify({'authorized': authorized, 'message': message})
# 		response.status_code = HTTPStatus.OK if authorized else HTTPStatus.UNAUTHORIZED
		# response = jsonify({'статус': 'ok'})
		# response.status_code = HTTPStatus.OK
		# return response


@ns.route('/register')
class RegisterAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Пользователь успешно зарегистрирован.')
	@ns.response(int(HTTPStatus.CONFLICT), 'Пользователь с таким именем уже существует.')
	@ns.response(int(HTTPStatus.BAD_REQUEST), 'Пароль не соответствует ограничениям.')
	@ns.expect(auth_from_form_reqparser)
	@ns.doc(
		description='Пароль должен содержать не менее 8 символов, в т.ч. один из спецсимволов "!@#$%^&*()-=_+", '
					'также в пароле должен присутствовать один заглавный и строчный символ, и минимум одна цифра.'
	)
	def post(self):
		"""Регистрация нового пользователя в системе"""
		form_data = auth_from_form_reqparser.parse_args()

		process_register_from_form(**form_data)
		response = jsonify({'message': 'Пользователь успешно зарегисрирован!'})
		response.status_code = HTTPStatus.OK
		return response
