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

	MIN_FEEDBACK_LEN = 100
	data = [f for f in data if len(f['text']) >= MIN_FEEDBACK_LEN]  # длина каждого комментария больше минимума
	comments = []
	classes = []
	class_mapper = lambda x: 0 if x <= 2 else 1
	LIMIT = 20_000 # 1_000_000_
	COMMENTS_PER_SCORE = int(LIMIT / 5)

	one_score_comments = list((f for f in data if f['val'] == 1))
	two_score_comments = list((f for f in data if f['val'] == 2))
	three_score_comments = list((f for f in data if f['val'] == 3))
	four_score_comments = list((f for f in data if f['val'] == 4))
	five_score_comments = list((f for f in data if f['val'] == 5))

	print(f'1: {len(one_score_comments)}')
	print(f'2: {len(two_score_comments)}')
	print(f'3: {len(three_score_comments)}')
	print(f'4: {len(four_score_comments)}')
	print(f'5: {len(five_score_comments)}')

	print('Total:', len(one_score_comments) + len(two_score_comments) + len(three_score_comments) + len(
		four_score_comments) + len(five_score_comments))

	# for one
	comments.extend([f['text'] for f in one_score_comments[:COMMENTS_PER_SCORE]])
	classes.extend([class_mapper(f['val']) for f in one_score_comments[:COMMENTS_PER_SCORE]])

	# for two
	comments.extend([f['text'] for f in two_score_comments[:COMMENTS_PER_SCORE]])
	classes.extend([class_mapper(f['val']) for f in two_score_comments[:COMMENTS_PER_SCORE]])

	# for three
	comments.extend([f['text'] for f in three_score_comments[:COMMENTS_PER_SCORE]])
	classes.extend([class_mapper(f['val']) for f in three_score_comments[:COMMENTS_PER_SCORE]])
	# for four
	comments.extend([f['text'] for f in four_score_comments[:COMMENTS_PER_SCORE]])
	classes.extend([class_mapper(f['val']) for f in four_score_comments[:COMMENTS_PER_SCORE]])
	# for five
	comments.extend([f['text'] for f in five_score_comments[:COMMENTS_PER_SCORE]])
	classes.extend([class_mapper(f['val']) for f in five_score_comments[:COMMENTS_PER_SCORE]])

	print('Total for train:',
		  len(one_score_comments[:COMMENTS_PER_SCORE]) + len(two_score_comments[:COMMENTS_PER_SCORE]) + len(
			  three_score_comments[:COMMENTS_PER_SCORE]) + len(
			  four_score_comments[:COMMENTS_PER_SCORE]) + len(five_score_comments[:COMMENTS_PER_SCORE]))

	print(list(zip(comments, classes))[:3])

	model = {
		"modelTitle": f"bag_words_{LIMIT}",
		"classifier": "logistic-regression",
		"tokenizerType": "nltk-tokenizer",
		"vectorizationType": "bag-of-words",
		"stopWords": [],
		"useDefaultStopWords": True,
		"excludeDefaultStopWords": ['не'],
		"punctuations": [
			"!", "?", ",", ".", ";",
			":", "..", "...", ")", "(",
			"]", "[", "@", "#", "$", "№",
			"^", "&", "*", "_", "+", "-"
		],
		"minTokenLength": 2,
		"deleteNumbers": True,
		"comments": comments,
		"classes": classes,
		"maxWords": 15_000
	}

	try:
		response = session.post(
			TRAIN_MODEL_URL,
			json=model,
			auth=(username, password),
			headers={"Connection": "close"}
		)
	except ConnectionError:
		print('Соединение разорвано!')

	status_code = response.status_code
	if status_code == 200:
		print(f'Пользователь {user["username"]} успешно обучил модель {model["modelTitle"]} системе!')
	else:
		print(f'Ошибка обучения модели у пользователя {user["username"]}, код {status_code}')
	print(response.content)


if __name__ == '__main__':
	USERNAME, PASSWORD = 'markeeff', '!@Markeeff1'
	if input('need register (y/n): ')[0].lower() == 'y':
		register_user(USERNAME, PASSWORD)
	else:
		print('Use default user: ', (USERNAME, PASSWORD))

	user = {'username': USERNAME, 'password': PASSWORD}
	dataset_filepath = 'Женщинам_Блузки и рубашки.json'
	user_train_model(user, dataset_filepath)
