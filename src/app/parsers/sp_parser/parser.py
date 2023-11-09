import aiohttp

import asyncio
from ..utilities.timer import Timer
from ..utilities import save_json_to_file
from .constants import COOKIES, HEADERS
from ..sp_parser.entities.pages_parser import PagesParser


async def main(url: str, pages: int):
	async with aiohttp.ClientSession(cookies=COOKIES, headers=HEADERS) as session:
		feedbacks = await PagesParser.parse_pages(session, url, pages)
		return feedbacks


if __name__ == '__main__':
	url = input('Введите ссылку на каталог для парсинга (например, "/catalog/zhenskaya_odezhda/kurtki/"): ')
	pages = int(input('Введите кол-во страниц, необходимых для парсинга (например, "2"): '))
	with Timer() as _:
		feedbacks = asyncio.run(main(url, pages))

	filename = '-'.join(url[1:-1].split('/')[1:])
	save_json_to_file([f for f in feedbacks], filename)
