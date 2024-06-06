from src.app.parsers.utilities import get_json_by_url
from src.app.parsers.wb_parser.entities.category import Category
from src.app.parsers.wb_parser.entities.exceptions import NoShardTagInCategoryExc


class WbMenu():
	""" Меню сайта Wildberries """

	def show(self, cat_sign='>', subcat_sing='\t|'):
		""" Вывод меню в формате Категория -> Подкатегории (у которых больше нет подкатегорий) """
		print('Меню Wildberries')
		for c in self.categories:
			print(cat_sign, c.name)
			if c.has_subcategories:
				for num2, sc in enumerate(c.subcategories, start=1):
					if not sc.has_subcategories:
						print(subcat_sing, sc.name)
	def get_menu(self):
		""" Получение меню в формате Категория -> Подкатегории """
		menu = {} # итоговое меню

		for c in self.categories: # по категории
			category = c.name
			subcategies = []  # её ^ подкатегории
			if c.has_subcategories: # если в категории есть подкатегории

				for sc in c.subcategories: # по подкатегории
					if not sc.has_subcategories: # если у подкатегории нет подкатегорий
						subcategies.append(sc.name)

				# если есть хотя бы одна подкатегория, то запоминаем
				if subcategies:
					menu = {**menu, **{category: subcategies}}


		return menu



	def __init__(self):
		menu_url = r'https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json'
		self.menu = []
		for c in get_json_by_url(menu_url):
			try:
				cat = Category(c)
			except NoShardTagInCategoryExc:
				pass
			else:
				self.menu.append(cat)

	@property
	def categories(self):
		""" Получение доступных категорий меню """
		return (c for c in self.menu)

	def get_category(self, category_name: str) -> dict or None:
		""" Получение категории по имени """
		try:
			cat = next(filter(lambda c: c.name == category_name, self.categories))
			return cat
		except StopIteration:
			return None
