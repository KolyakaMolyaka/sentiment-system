class LoadTrainInfoFacade:
	""" Фасад для загрузки информации об обученной модели """

	def get_model_info(cls, username: str, model_title: str):
		pass

	def _load_model(self,):

	def load_model(model_title):
		# load user model by its title
		db_user = User.query.filter_by(username=request.authorization.username).one_or_none()
		filename = os.path.join(current_app.config['TRAINED_MODELS'], db_user.username, model_title, 'model.pkl')
		with open(filename, 'rb') as f:
			ml_model = pickle.load(f)
			return ml_model

	def load_stop_words(model_title):
		# Загрузка стоп-слов, которые использовал пользователь при обучении модели
		db_user = User.query.filter_by(username=request.authorization.username).one_or_none()
		filename = os.path.join(current_app.config['TRAINED_MODELS'], db_user.username, model_title, 'stop_words.csv')
		stop_words = []
		with open(filename) as csvfile:
			csvreader = csv.reader(csvfile, delimiter=';')
			for row in csvreader:  # формат следующий: ['row']
				stop_words.extend(row)

		return stop_words
