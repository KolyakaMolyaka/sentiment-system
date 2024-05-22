from src.app.ext.database.models import MlModel, User
from flask import request, abort
from http import HTTPStatus
def process_model_delete_request(model_title):
	user = User.query.filter_by(username=request.authorization.username).one_or_none()
	model = MlModel.query.filter_by(model_title=model_title, user_id=user.id).one_or_none()
	if not model:
		abort(int(HTTPStatus.NOT_FOUND), f'модель {model_title} не найдена')

	# delete model from db
	MlModel.delete_model(model_title)
	# delete model folder
	# check train_model_logic.py for modelsdir_path
	import shutil
	username = request.authorization.username
	dir_path = '/usr/src/app/src/app/core/train_model'
	modelsdir_path = '/models'
	# import os
	# os.path.join('..', 'train_model', 'models', username, model_title)
	directory = dir_path + rf'{modelsdir_path}/{username}/{model_title}/'
	shutil.rmtree(directory)

