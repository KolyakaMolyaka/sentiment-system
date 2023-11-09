import os
import time

from flask import Blueprint, request, render_template, send_file, current_app
from .form import CreateSportmasterDatasetForm

bp = Blueprint('create_datasets', __name__, template_folder='templates')


@bp.route('/create_sportmaster_dataset', methods=['GET', 'POST'])
async def create_dataset():
	if request.method == 'GET':
		form = CreateSportmasterDatasetForm()

		return render_template(
			'create_sportmaster_dataset.html',
			form=form
		)

	form = CreateSportmasterDatasetForm(request.form)
	d = form.data
	pages = d.get('pages')
	catalog_url = d.get('catalog_url')

	# логика
	from src.app.parsers.sp_parser.parser import main, save_json_to_file
	feeds = await main(catalog_url, pages)
	filename = '-'.join(catalog_url[1:-1].split('/')[1:])
	save_json_to_file([f for f in feeds], 'saved_datasets/' + filename)
	uploads = os.path.join(current_app.root_path, 'saved_datasets')

	# отладка
	print(uploads)
	print(filename + '.json')

	# отправка файла
	return send_file(uploads + '/' + filename + '.json', as_attachment=True)

@bp.route('/sleep')
async def sleeping():
	time.sleep(5)
	return 'slept 5 secs'
