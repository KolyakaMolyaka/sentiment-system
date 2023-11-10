from flask import Flask


def create_app():
	app = Flask(__name__)

	"""Configurations"""
	# take environment variables from .env
	from dotenv import load_dotenv
	load_dotenv()
	app.config.from_prefixed_env()

	"""Routes"""
	# create datasets routes
	from .routes.create_datasets import bp as create_datasets_bp
	app.register_blueprint(create_datasets_bp)

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

	from .commands.commands import init_db_command
	app.cli.add_command(init_db_command)

	return app
