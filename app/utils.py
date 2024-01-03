import asyncio
import re

import aiohttp
from aiogram.types import URLInputFile, Message
from aiogram_dialog import DialogManager
from bs4 import BeautifulSoup

from app import config
from app.keyboards.keyboards import book_selection_kb
from main import bot


async def send_solution(message: Message, result: dict[str: str], dialog_manager: DialogManager):
	if not result:
		# Обработка случая, когда решение не найдено
		await message.answer('Не найдено 😕')
	else:
		# Извлечение решения и заголовка из результата
		solution, title = result.get('solution'), result.get('title')
		if isinstance(solution, str):
			# Если решение представляет собой текст, разбиваем и отправляем его
			await send_split_text(message, solution)
		elif isinstance(solution, list):
			# Если решение - список URL-адресов, отправляем их соответственно
			await send_solution_urls(message, solution, title)
		await message.answer(title)
	await dialog_manager.done()


async def send_split_text(message: Message, solution: str):
	for text in split_text(solution):
		await message.answer(text)
		await asyncio.sleep(config.MESSAGE_DELAY)


async def send_solution_urls(message: Message, solution: list[str], title: str):
	for url in solution:
		if url.startswith('https://'):
			# Если URL - изображение, отправляем его как фото
			image = URLInputFile(url, filename=title)
			await bot.send_photo(chat_id=message.chat.id, photo=image)
		else:
			# Если это аннотация, то отправляем текст
			await message.answer(url)
		await asyncio.sleep(config.MESSAGE_DELAY)


def split_text(text: str, max_length: int = 4096) -> list[str]:
	# Находим границы предложений и абзацев
	boundaries = list(re.finditer(r'(?<=[.!?])\s+|\n', text))

	# Добавляем начало и конец текста в границы
	boundaries = [(-1, 0)] + [(m.start(), m.end()) for m in boundaries] + [(len(text), len(text))]

	# Объединяем предложения и абзацы, пока они не достигнут максимальной длины
	parts = []
	start = 0
	for i in range(1, len(boundaries)):
		if boundaries[i][0] - start > max_length:
			parts.append(text[start:boundaries[i - 1][1]])
			start = boundaries[i - 1][1]
	parts.append(text[start:])
	return parts


class PageParser:
	def __init__(self, parse_url: str) -> None:
		self.parse_url = parse_url

	@staticmethod
	async def parse_page(parse_url: str) -> BeautifulSoup | None:
		async with aiohttp.ClientSession() as session:
			async with session.get(parse_url, headers=config.HEADERS) as response:
				if response.status == 404:
					return None
				page = await response.text()
				return BeautifulSoup(page, 'html.parser')

	async def parse_gdz(self) -> list[str] | None:
		soup = await self.parse_page(self.parse_url)
		if not soup:
			return None
		solutions_url = ['https:' + div.img['src'] for div in soup.find_all('div', class_='with-overtask')]
		return solutions_url or ['https://gdz.ru' + soup.find('div', class_='task-img-container').img['src']]

	async def parse_resheba(self) -> str | None:
		soup = await self.parse_page(self.parse_url)
		if not soup:
			return None
		solution_text = [p.getText() for p in soup.find_all('div', class_='taskText')]
		return ''.join(solution_text).replace('\n\n', '\n')

	async def parse_reshak(self) -> list[str] | None:
		soup = await self.parse_page(self.parse_url)
		if not soup:
			return None
		result = []
		for el in soup.find_all('h2', class_='titleh2'):
			result.append(el.get_text())
			img_link = el.find_next('div').img.get('src', '') or el.find_next('div').img.get('data-src', '')
			result.append('https://reshak.ru/' + img_link)
		return result


def get_annotation_text(book: str = None, **kwargs) -> str:
	base_text = f'Это все, что мне удалось найти по запросу:\n\nУчебник: ***{book}***\n' if book else ''
	additional_info = '\n'.join(
		[f'{key.capitalize()}: ***{value}***' for key, value in kwargs.items()]) if kwargs else ''
	return base_text + additional_info
