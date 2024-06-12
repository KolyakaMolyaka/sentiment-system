from constants import HOST, API_URL


class CreateUrl:
	@property
	def ulr(self):
		return self.url

	def __init__(self, controller_url):
		assert controller_url[0] == '/', f'{controller_url} должно начинаться с "/"'
		self.url = HOST + API_URL + controller_url
