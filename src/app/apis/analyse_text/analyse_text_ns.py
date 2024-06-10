from http import HTTPStatus
from flask import jsonify
from flask_restx import Resource, Namespace
from src.app.core.sentiment_analyse.analyse_logic import process_analyse_text

from .dto import sentiment_model

ns = Namespace(
	name='Sentiment Analyse Controller',
	description='Анализ тональностью текста на основе предобученных моделей',
	path='/sentiment_analyse/',
	validate=True
)


@ns.route('/analyse_text')
class SentimentAnalyseAPI(Resource):
	@ns.response(int(HTTPStatus.OK), 'Оценка тональности.')
	@ns.response(int(HTTPStatus.BAD_REQUEST), 'Неизвестный тип модели.')
	@ns.doc(
		description='Оценка тональности текста на основе предобученных моделей. '
					'Текст должен относиться к предметной области "Блузки и рубашки", в противном случае '
					'корректность тональности не гарантируется.'
	)
	@ns.expect(sentiment_model)
	def post(self):
		""" Анализ тональности текста при помощи предобученных моделей """

		d = ns.payload

		model_type = d.get('modelType')
		text = d.get('text')

		sentiment_description = process_analyse_text(model_type, text)

		extra_info = {
			'text': text,
			'modelType': model_type
		}
		response = jsonify({
			**sentiment_description, **extra_info
		})
		response.status_code = HTTPStatus.OK

		return response
