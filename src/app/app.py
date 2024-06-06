from flask import Flask
import os


def create_app():
	app = Flask(__name__)

	"""Configurations"""
	# take environment variables from .env
	from dotenv import load_dotenv
	load_dotenv()
	app.config.from_prefixed_env()


	""" Upload folder """
	UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
	app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
	app.config['PRETRAINED_MODELS'] = os.path.join(UPLOAD_FOLDER, 'pretrained_models')
	app.config['TRAINED_MODELS'] = os.path.join(UPLOAD_FOLDER, 'models')

	os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
	os.makedirs(app.config['TRAINED_MODELS'], exist_ok=True)
	os.makedirs(app.config['PRETRAINED_MODELS'], exist_ok=True)

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

	from .commands.commands import init_db_command, fill_db_command, download_nltk_data_command, download_navec_data_command
	app.cli.add_command(init_db_command)
	app.cli.add_command(fill_db_command)
	app.cli.add_command(download_nltk_data_command)
	app.cli.add_command(download_navec_data_command)

	return app
