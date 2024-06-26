import os.path
import shutil
import nltk
import wget
import click
from flask.cli import with_appcontext
from flask import current_app
from src.app.ext.database import db
from src.app.ext.database.models import Tokenizer, Vectorization


@click.command('delete-previous-models')
@with_appcontext
def delete_previous_models_command():
	""" Clear previous saved models """

	trained_models_filepath = current_app.config['TRAINED_MODELS']
	for file in os.listdir(trained_models_filepath):
		filepath = os.path.join(current_app.config['TRAINED_MODELS'], file)
		shutil.rmtree(filepath)

	click.echo(f'Directory {trained_models_filepath} was cleared!')


@click.command('init-db')
@with_appcontext
def init_db_command():
	db.drop_all()
	db.create_all()
	db.session.commit()
	click.echo('Database initialized.')


@click.command('download-nltk-data')
def download_nltk_data_command():
	nltk.download('punkt')
	nltk.download('stopwords')
	click.echo('NLTK punkt and stopwords data are downloaded.')


@click.command('download-navec-data')
def download_navec_data_command():
	url = 'https://storage.yandexcloud.net/natasha-navec/packs/navec_hudlit_v1_12B_500K_300d_100q.tar'
	navec_filename = 'navec_hudlit_v1_12B_500K_300d_100q.tar'
	if not os.path.exists(navec_filename):
		filename = wget.download(url)
		click.echo(f'Navec data downloaded in {filename}')
	else:
		click.echo(f'Navec is already downloaded in {navec_filename}')


@click.command('fill-db')
@with_appcontext
def fill_db_command():
	""" Заполнение БД данными по умолчанию """

	unknown_tokenizer = Tokenizer(
		title='unknown',
		description='Неизвестный токенизатор. Пользователь обучал модель с помощью собственных векторов.'
	)
	unknown_tokenizer.save()

	# Информация о токенизаторах
	nltk_tokenizer = Tokenizer(
		title='nltk-tokenizer',
		description='Токенизатор доступен благодаря библиотеке NLTK и функции nltk.tokenize.word_tokenize(), '
					'с помощью которой получаются токены. Функция возвращает слоги из одного слова, '
					'а одно слово может содержать один или больше слогов.'
	)
	nltk_tokenizer.save()

	default_whitespace_tokenizer = Tokenizer(
		title='default-whitespace-tokenizer',
		description='Токенизатор реализуется функцией split в Python применённой к строке с текстом. Это означает, что '
					'токены выделяются путём разделения строки пробельным символом.',
	)
	default_whitespace_tokenizer.save()

	word_punck_tokenizer = Tokenizer(
		title='wordpunct-tokenizer',
		description='Используется токенизация текста функции nltk.tokenize.wordpunct_tokenize() из библиотеки NLTK. '
					'Функция возвращает токены путём разбиения текста по пробелам и с учетом знаков препинания.',
	)
	word_punck_tokenizer.save()

	# Информация о методах векторизации

	unknown_vectorization = Vectorization(
		title='unknown',
		description='Неизвестный метод векторизации. Пользователь самостоятельно получал векторы и обучал модель на их основе.'
	)
	unknown_vectorization.save()

	bag_of_words_alg = Vectorization(
		title='bag-of-words',
		description='Векторизация текста при помощи алгоритма "Мешок слов". '
					'Вектор содержит столько элементов, сколько анализируемых слов (возможно ограничение кол-ва анализируемых слов). '
					'Каждому слову присваивается код, который будет обозначать это слово. Присутствуют дополнительные коды: '
					'0 - код заполнитель (используется для увеличения вектора до фиксированной длины), '
					'1 - код, обозначающий неизвестное слово (в случае ограничения кол-ва анализируемых слов). '
					'Каждый элемент вектора соответствует определенному слову, а значение равно количеству раз, '
					'сколько слово встречается в тексте.',
	)
	bag_of_words_alg.save()

	embeddings_alg = Vectorization(
		title='embeddings',
		description='Векторизация текста при помощи плотного векторного представления. '
					'Каждому токену соответствует вектор фиксированной длины. '
					'Элементами вектора могут быть любые действительные числа. '
					'Реализуется при помощи библиотеки Navec.'
	)
	embeddings_alg.save()

	click.echo('Tokenizers and Vectorizations are filled in database.')
