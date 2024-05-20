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
		except:
			abort(int(HTTPStatus.UNAUTHORIZED), 'Пользователь не авторизован.')
		process_login_from_form(username, password)

		return f(*args, **kwargs)

	return decorator


def process_login_from_form(username: str, password: str):
	u = User.query.filter_by(username=username).one_or_none()
	if not u:
		unauthorized = (int(HTTPStatus.NOT_FOUND), 'Неправильное имя пользователя или пароль')
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
