from flask import Flask

# import nltk
#
# nltk.download('punkt')
# nltk.download('stopwords')
#
# from navec import Navec
# import wget
#
# url = 'https://storage.yandexcloud.net/natasha-navec/packs/navec_hudlit_v1_12B_500K_300d_100q.tar'
# filename = wget.download(url)
# navec = Navec.load(filename)

def create_app():
	app = Flask(__name__)

	"""Configurations"""
	# take environment variables from .env
	from dotenv import load_dotenv
	load_dotenv()
	app.config.from_prefixed_env()

	"""Extensions"""

	# sqlalchemy
	from .ext.database import db
	db.init_app(app)

	# swagger
	from .apis import api
	api.init_app(app)

	# celery
	from src.app.ext.celery.make_celery import celery_init_app
	celery_init_app(app)

	from .commands.commands import init_db_command, fill_db_command
	app.cli.add_command(init_db_command)
	app.cli.add_command(fill_db_command)

	return app
