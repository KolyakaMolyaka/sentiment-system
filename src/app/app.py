from flask import Flask


def create_app():
	app = Flask(__name__)
	app.config.from_prefixed_env()

	from .routes.create_datasets import bp as create_datasets_bp
	app.register_blueprint(create_datasets_bp)

	# swagger
	from .apis import api
	api.init_app(app)

	# celery
	from src.app.ext.celery.make_celery import celery_init_app
	app.config['CELERY'] = {
		'broker_url': 'redis://localhost',
		'result_backend': 'redis://localhost',
		'task_ignore_result': True
	}
	app.config.from_prefixed_env()
	celery_init_app(app)
	return app
