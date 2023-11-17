from http import HTTPStatus
from flask import jsonify
from flask_restx import Resource, Namespace
from src.app.core.train_model.train_model_logic import train_model_logic
import pandas as pd

from .dto import train_model

ns = Namespace(
	name='Model Train Controller',
	description='Обучение модели',
	path='/model_train/',
	validate=True
)


@ns.route('/train_with_teacher')
class ModelTrainWithTeatherAPI(Resource):
	@ns.response(int(HTTPStatus.BAD_REQUEST), 'Different lengths of comments and classes')
	@ns.expect(train_model)
	@ns.doc(
		desctiption='Here you can train models.'
	)
	def post(self):
		d = ns.payload

		comments = d.get('comments')
		classes = d.get('classes')

		if len(comments) != len(classes):
			response = jsonify({
				'error': 'Lengths of comments and classes are differen.'
			})
			response.status_code = HTTPStatus.BAD_REQUEST
			return response

		for c in classes:
			if c not in (0, 1):
				response = jsonify({
					'error': 'Classes can be only 0 - negative, 1 - positive.'
				})
				response.status_code = HTTPStatus.BAD_REQUEST
				return response

		train_info = list(zip(comments, classes))
		df = pd.DataFrame(train_info, columns=['text', 'score'])
		trained_meta = train_model_logic(df, 10)
		response = jsonify({
			**d, **trained_meta
		})
		response.status_code = HTTPStatus.OK

		return response
