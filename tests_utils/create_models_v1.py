import requests
from constants import USERS, MODELS
from create_url import CreateUrl


def user_create_model(user):
	TRAIN_MODEL_URL = CreateUrl('/model_train/train_with_teacher/v1').url


	username = user['username']
	password = user['password']

	print(f'Создание модели пользователем {username}..')

	session = requests.Session()
	session.auth = (user, password)

	for model in MODELS:
		response = session.post(
			TRAIN_MODEL_URL,
			json=model,
			auth=(username, password),
			headers={"Connection": "close"}
		)

		status_code = response.status_code
		if status_code == 200:
			print(f'Пользователь {user["username"]} успешно обучил модель {model["modelTitle"]} системе!')
		else:
			print(f'Ошибка обучения модели у пользователя {user["username"]}, код {status_code}')
			print(response.content)


def create_models_in_system():
	for user in USERS:
		user_create_model(user)


if __name__ == '__main__':
	create_models_in_system()
