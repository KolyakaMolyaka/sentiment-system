from src.app.ext.database import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(128), nullable=False, unique=True)
	password = db.Column(db.Text(), nullable=False)
	ml_models = db.relationship("MlModel", backref="user", lazy='dynamic')

	@classmethod
	def get(cls, username):
		""" Получение экземпляра пользователя по username """
		u = User.query.filter_by(username=username).one_or_none()
		return u


	def __repr__(self):
		return f'<User: username={self.username}>'

	def set_password(self, password):
		self.password = generate_password_hash(password)

	def check_password(self, password):
		""" Проверка, совпадает ли переданный пароль с настоящим """
		return check_password_hash(self.password, password)

	def save(self):
		""" Запись изменений пользователя в БД """
		db.session.add(self)
		db.session.commit()
