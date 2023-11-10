import os
import aiohttp
from flask import current_app
from celery import shared_task, states
from celery.exceptions import Ignore
import asyncio

from src.app.parsers.sp_parser.parser import main as parse_sportmaster_site


def process_create_sportmaster_dataset(catalog_url: str, pages: int):
	"""Create task for getting dataset"""

	result = create_sportmaster_dataset.delay(catalog_url, pages)
	return result


@shared_task(bind=True, ignore_result=False)
def create_sportmaster_dataset(self, catalog_url: str, pages: int):
	try:
		feeds = asyncio.run(parse_sportmaster_site(catalog_url, pages))
	except aiohttp.ContentTypeError:
		self.update_state(
			state=states.FAILURE,
		)
		# ignore the task so no other state is recorded
		raise Ignore()

	return [f for f in feeds]
