import asyncio
import aiohttp
from src.app.parsers.wb_parser.entities.wbmenu import WbMenu
from src.app.parsers.wb_parser.entities.category_parser import CategoryParser


async def main(category_name: str, subcategory_name: str, pages=10):
	print('Запуск парсинга!')
	menu = WbMenu()
	cat = menu.get_category(category_name)
	sc = cat.get_subcategory(subcategory_name)
	async with aiohttp.ClientSession() as session:
		feedbacks = await CategoryParser.parse(sc, session, pages=pages)
		result_filename = category_name + '_' + subcategory_name

	# save_json_to_file([f for f in feedbacks], result_filename)
	return feedbacks


if __name__ == '__main__':
	menu = WbMenu()
	menu.show()
	category_name = input('Введите название категории для парсинга (например, "Женщинам"): ')
	subcategory_name = input('Введите подкатегорию для парсинга (например, "Блузки и рубашки"): ')
	pages = int(input('Введите кол-во страниц (например, "2"): '))

	feedbacks = asyncio.run(main(menu, category_name, subcategory_name, pages))
