# команда создания БД
import click
from flask.cli import with_appcontext
from src.app.ext.database import db


@click.command('init-db')
@with_appcontext
def init_db_command():
	db.drop_all()
	db.create_all()
	db.session.commit()
	click.echo('Database initialized.')
