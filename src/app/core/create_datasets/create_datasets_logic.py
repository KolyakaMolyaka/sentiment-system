from celery import shared_task
import asyncio

from src.app.parsers.sp_parser.parser import main as parse_sportmaster_site


@shared_task(ignore_result=False)
def add_together(a: int, b: int) -> int:
	return a + b


@shared_task(ignore_result=False)
def create_sportmaster_dataset(catalog_url: str, pages: int):
	feeds = asyncio.run(parse_sportmaster_site(catalog_url, pages))
	return [f for f in feeds]
