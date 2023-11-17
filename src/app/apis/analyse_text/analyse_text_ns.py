from flask_restx import Resource, Namespace

ns = Namespace(
	name='Sentiment Analyse Controller',
	description='Анализ тональностью текста',
	path='/sentiment_analyse/',
	validate=True
)


# @ns.route('/analyse_text')
class SentimentAnalyseAPI(Resource):
	def post(self):
		""" Analyse text with prepared models """
		return 'sentiment result'
