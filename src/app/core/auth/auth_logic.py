from functools import wraps
from http import HTTPStatus
from flask import abort, request
from src.app.ext.database.models import User


def requires_auth(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		# validate username and password
		auth = request.authorization
		try:
			username = getattr(auth, 'username')
			password = getattr(auth, 'password')
			print('credentials:', username, password)
			# проверка, правильный ли логин и пароль
			process_login_from_form(username, password)
		except:
			abort(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не авторизован.')

		return f(*args, **kwargs)

	return decorator


def process_login_from_form(username: str, password: str):
	u = User.query.filter_by(username=username).one_or_none()

	unauthorized = (int(HTTPStatus.NOT_FOUND), 'Неправильное имя пользователя или пароль')
	if not u:
		abort(*unauthorized)

	if u.check_password(password) == False:
		abort(*unauthorized)

	# log in user ...
	return


def process_register_from_form(username: str, password: str):
	already_exist_user = User.query.filter_by(username=username).one_or_none()
	if already_exist_user:
		abort(int(HTTPStatus.CONFLICT), f'{username} уже существует.')

	u = User(username=username, is_admin=False)
	u.set_password(password)
	u.save()

def process_user_check_authorization():
	authorized = False
	auth = request.authorization
	print(auth)
	if not auth:
		message = 'нет заголовка authorization'
		return authorized, message

	username, password = getattr(auth, 'username', None), getattr(auth, 'password', None)
	if not username or not password:
		message = 'нет username или password в заголовке authorization'
		return authorized, message

	u = User.query.filter_by(username=username).one_or_none()
	if not u:
		message = 'пользователь с username не существует'
		return authorized, message

	if not u.check_password(password):
		message = f'пользователь {username} имеет другой пароль!'
		return authorized, message

	authorized = True
	message = 'вы авторизованы!'
	return authorized, message