from src.app.ext.database import db


class Vectorization(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128), nullable=False, unique=True)
	description = db.Column(db.Text(), nullable=False)
	is_archived = db.Column(db.Boolean, default=False)

	ml_models = db.relationship('MlModel', backref='vectorization')

	@classmethod
	def get(cls, title):
		""" Получение экземпляра векторизации по title """
		u = Vectorization.query.filter_by(title=title).one_or_none()
		return u

	@classmethod
	def get_by_id(cls, id: int):
		v = Vectorization.query.filter_by(id=id).one_or_none()
		return v

	def __repr__(self):
		return f'<Vectorization: title={self.title}>'

	def save(self):
		""" Запись изменений пользователя в БД """
		db.session.add(self)
		db.session.commit()
