import random

import requests
import json
from create_url import CreateUrl


def register_user(username, password):
	REGISTER_USER_URL = CreateUrl('/auth/register').url
	HEADERS = {'Content-Type': 'application/x-www-form-urlencoded'}
	user = {'username': username, 'password': password}
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


def user_train_model(user: dict, dataset_filepath: str):
	TRAIN_MODEL_URL = CreateUrl('/model_train/train_with_teacher/v1').url

	username = user['username']
	password = user['password']

	print(f'Создание модели пользователем {username}..')

	session = requests.Session()
	session.auth = (user, password)

	with open(dataset_filepath, 'r', encoding='utf-8') as f:
		data = json.load(f)

	comments = []
	classes = []
	class_mapper = lambda x: 0 if x <= 3 else 1
	LIMIT = 1_000_000
	for feedback in data[:LIMIT]:
		comment = feedback['text']
		val = feedback['val']
		comment_class = class_mapper(val)
		comments.append(comment)
		classes.append(comment_class)

	print(list(zip(comments, classes))[:3])

	model = {
		"modelTitle": "my_pretrained_model2",
		"classifier": "logistic-regression",
		"tokenizerType": "nltk-tokenizer",
		"vectorizationType": "bag-of-words",
		"stopWords": [],
		"useDefaultStopWords": True,
		"excludeDefaultStopWords": ['не'],
		"punctuations": [
			"!",
			"?",
			",",
			".",
			";",
			":",
			"..",
			"..."
		],
		"minTokenLength": 2,
		"deleteNumbers": True,
		"comments": comments,
		"classes": classes,
		"maxWords": 10_000
	}

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


if __name__ == '__main__':
	USERNAME, PASSWORD = 'markeeff', '!@Markeeff1'
	# register_user(USERNAME, PASSWORD)
	user = {'username': USERNAME, 'password': PASSWORD}
	dataset_filepath = 'Женщинам_Блузки и рубашки.json'
	user_train_model(user, dataset_filepath)
