import requests
from constants import USERS
from create_url import CreateUrl


def create_users_in_system():
	REGISTER_USER_URL = CreateUrl('/auth/register').url
	HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
	for user in USERS:
		response = requests.post(
			REGISTER_USER_URL,
			data=user,
			headers=HEADERS
		)

		status_code = response.status_code
		if status_code == 200:
			print(f'Пользователь {user["username"]} успешно зарегистрирован в системе!')
		else:
			print(f'Ошибка добавления пользователя {user["username"]}, код {status_code}')


if __name__ == '__main__':
	create_users_in_system()
