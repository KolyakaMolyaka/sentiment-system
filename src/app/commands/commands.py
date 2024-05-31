# команда создания БД
import click
from flask.cli import with_appcontext
from src.app.ext.database import db
from src.app.ext.database.models import Tokenizer, Vectorization


@click.command('init-db')
@with_appcontext
def init_db_command():
	db.drop_all()
	db.create_all()
	db.session.commit()
	click.echo('Database initialized.')


@click.command('fill-db')
@with_appcontext
def fill_db_command():
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


	pass
