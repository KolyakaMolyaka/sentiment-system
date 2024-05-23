from src.app.ext.database import db

class MlModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	model_title = db.Column(db.String(128), nullable=False)
	model_accuracy = db.Column(db.Float, nullable=False)
	classifier = db.Column(db.String(128), nullable=False)

	tokenizer_type = db.Column(db.String(128), nullable=False)
	vectorization_type = db.Column(db.String(128), nullable=False)
	use_default_stop_words = db.Column(db.Boolean, nullable=False)

	max_words = db.Column(db.Integer, nullable=False)

	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

	def __repr__(self):
		return f'<Model: title={self.model_title}>'

	def save(self):
		""" Запись изменений в БД """
		db.session.add(self)
		db.session.commit()

	@classmethod
	def delete_model(cls, model_title):
		""" Удаление модели из БД """
		model = MlModel.query.filter_by(model_title=model_title)
		model.delete()
		# db.session.delete(model)
		db.session.commit()

