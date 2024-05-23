import asyncio
import aiohttp
from src.app.parsers.wb_parser.entities.wbmenu import WbMenu
from src.app.parsers.wb_parser.entities.category_parser import CategoryParser
from src.app.parsers.utilities import save_json_to_file
from src.app.parsers.utilities.timer import Timer


async def main(category_name: str, subcategory_name: str, pages=10, menu: WbMenu = WbMenu()):
	print(menu.show())
	print('task category name', category_name)
	print('task subcategory name', subcategory_name)
	cat = menu.get_category(category_name)
	sc = cat.get_subcategory(subcategory_name)
	# sc = cat.get_subcategory('Брюки')
	async with aiohttp.ClientSession() as session:
		feedbacks = await CategoryParser.parse(sc, session, pages=pages)
		print('task parsed feedbacks', feedbacks)
		return feedbacks


if __name__ == '__main__':
	menu = WbMenu()
	menu.show()
	category_name = input('Введите название категории для парсинга (например, "Женщинам"): ')
	subcategory_name = input('Введите подкатегорию для парсинга (например, "Блузки и рубашки"): ')
	pages = int(input('Введите кол-во страниц (например, "2"): '))

	result_filename = category_name + '_' + subcategory_name
	with Timer() as _:
		feedbacks = asyncio.run(main(category_name, subcategory_name, pages, menu))

	save_json_to_file([f for f in feedbacks], result_filename)
