from functools import wraps
from http import HTTPStatus
from flask import abort, request
from src.app.ext.database.models import User


def requires_auth(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		unauthorized = {'error': 'Invalid username or password.'}, HTTPStatus.UNAUTHORIZED
		# validate username and password
		auth = request.authorization
		if not auth:
			return unauthorized

		u = User.query.filter_by(username=auth.username).one_or_none()
		if not u:
			return unauthorized

		if u.check_password(auth.password) == False:
			return unauthorized

		return f(*args, **kwargs)

	return decorator


def process_login_from_form(username: str, password: str):
	pass


def process_register_from_form(username: str, password: str):
	already_exist_user = User.query.filter_by(username=username).one_or_none()
	if already_exist_user:
		abort(int(HTTPStatus.CONFLICT), f'{username} is already exists.')

	u = User(username=username, is_admin=False)
	u.set_password(password)
	u.save()
