from src.app.ext.database import db


class Tokenizer(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(128), nullable=False, unique=True)
	description = db.Column(db.Text(), nullable=False)
	is_archived = db.Column(db.Boolean, default=False)

	@classmethod
	def get(cls, title):
		""" Получение экземпляра токенизатора по title """
		u = Tokenizer.query.filter_by(title=title).one_or_none()
		return u

	def __repr__(self):
		return f'<Tokenizer: title={self.title}>'

	def save(self):
		""" Запись изменений пользователя в БД """
		db.session.add(self)
		db.session.commit()
