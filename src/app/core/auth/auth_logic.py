from functools import wraps
from http import HTTPStatus
from flask import abort, request
from src.app.ext.database.models import User


def requires_auth(f):
	@wraps(f)
	def decorator(*args, **kwargs):
		# Требование к авторизованному доступу
		auth = request.authorization
		if not auth:
			abort(int(HTTPStatus.UNAUTHORIZED), 'В HTTP запросе отсутствует заголовок Authorization, '
												'добавьте заголовок с реквизитами username и password для авторизации.')

		username, password = getattr(auth, 'username', None), getattr(auth, 'password', None)
		if not username or not password:
			abort(int(HTTPStatus.UNAUTHORIZED), 'В заголовке Authorization отсутствует реквизит username или password.')

		password_check(password)

		u = User.query.filter_by(username=username).one_or_none()
		if not u:
			abort(int(HTTPStatus.UNAUTHORIZED), f'Пользователь с таким {username} не зарегистрирован в системе.')

		if not u.check_password(password):
			abort(int(HTTPStatus.UNAUTHORIZED), f'Вы ввели неправильный пароль для пользователя {username}!')

		return f(*args, **kwargs)

	return decorator

def password_check(password: str):
	""" Проверка надёжности """

	MIN_PASSWORD_LEN = 8
	special_sym = list('!@#$%^&*()-=_+')

	# длина пароля
	if len(password) < MIN_PASSWORD_LEN:
		abort(int(HTTPStatus.BAD_REQUEST), f'Длина пароля должна быть не меньше {MIN_PASSWORD_LEN} символов')

	# наличие заглавной буквы
	if not any(ch.isupper() for ch in password):
		abort(int(HTTPStatus.BAD_REQUEST), 'Хотя бы один символ в пароле должен быть заглавной буквой')

	# наличие строчной буквы
	if not any(ch.islower() for ch in password):
		abort(int(HTTPStatus.BAD_REQUEST), 'Хотя бы один символ в пароле должен быть строчной буквой')

	# наличие спецсимвола
	if not any(ch in special_sym for ch in password):
		abort(int(HTTPStatus.BAD_REQUEST), f'Хотя бы один символ в пароле должен быть из списка: "{special_sym}"')

	return True


def process_register_from_form(username: str, password: str):
	already_exist_user = User.query.filter_by(username=username).one_or_none()
	if already_exist_user:
		abort(int(HTTPStatus.CONFLICT), f'{username} уже существует.')

	u = User(username=username)
	password_check(password)
	u.set_password(password)
	u.save()