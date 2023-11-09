from wtforms import Form, StringField, SubmitField, IntegerField, RadioField


class CreateSportmasterDatasetForm(Form):
	catalog_url = StringField('URL каталога', render_kw={'value': '/catalog/zhenskaya_odezhda/kurtki/'})
	pages = IntegerField('Количество страниц', render_kw={'value': '2'})
	format = RadioField('Формат файла', choices=(('json', 'json'), ('csv', 'csv')))
	submit = SubmitField('Начать парсинг')
