import asyncio
import re

import aiohttp
from aiogram.types import Message, URLInputFile
from bs4 import BeautifulSoup

from app import config
# from app.parser import get_solve
from main import bot


class Parser:
	def __init__(self, book: str, numbering: str) -> None:
		self.book = book
		self.numbering = numbering

		self.__subject_url = ''
		self.__parser_engine = config.PARSER_ENGINE

	async def get_solution_data(self) -> None | dict[str, str]:
		subject = self.book.split()[0].lower()

		if subject == 'английский':
			self.__subject_url = rf'https://gdz.ru/class-10/english/reshebnik-spotlight-10-afanaseva-o-v/{self.numbering}-s/'
		elif subject == 'русский':
			self.__subject_url = rf'https://gdz.ru/class-10/russkii_yazik/vlasenkov-i-rybchenkova-10-11/{self.numbering}-nom/'
		elif subject == 'алгебра-задачник' and re.match(config.ALGEBRA_NUMBER_PATTERN, self.numbering):
			parts_of_number = self.numbering.split('.')
			self.__subject_url = (
				rf'https://gdz.ru/class-10/algebra/reshebnik-mordkovich-a-g/{parts_of_number[0]}-item-'
				rf'{parts_of_number[1]}/')
		elif subject == 'геометрия':
			class_number = '10' if int(self.numbering) < 400 else '11'
			self.__subject_url = rf'https://gdz.ru/class-10/geometria/atanasyan-10-11/{class_number}-class-{self.numbering}/'
		elif subject == 'обществознание':
			self.__subject_url = rf'https://resheba.me/gdz/obshhestvoznanie/10-klass/soboleva/paragraph-{self.numbering}'
			self.__parser_engine = 'resheba.ru'
		else:
			return None

		result = await self.__parse_solution()
		if result:
			return {'solution': result, 'title': get_title(self.book, self.numbering)}
		return None

	async def __parse_solution(self) -> list[str] | str | None:
		"""Значения, которые может вернуть метод
			list[str]: Решение в виде фотографий с сайта gdz.ru
			str: Решение обществознания, которое берется с сайта resheba.ru
			"""
		if self.__subject_url:
			if self.__parser_engine == 'gdz.ru':
				return await self.__parse_gdz()
			elif self.__parser_engine == 'resheba.ru':
				return await self.__parse_resheba()

	async def __parse_gdz(self) -> None | list[str]:
		async with aiohttp.ClientSession() as session:
			async with session.get(self.__subject_url, headers=config.HEADERS) as response:
				if response.status == 404:
					return None

				text = await response.text()
				soup = BeautifulSoup(text, 'html.parser')

				# Url фоток с решениями
				solutions_url: list[str] = ['https:' + div.img['src'] for div in
				                            soup.find_all('div', class_='with-overtask')]

				if not solutions_url:
					no_solution: list[str] = [
						'https://gdz.ru' + soup.find('div', class_='task-img-container').img['src']]
					return no_solution

				return solutions_url

	async def __parse_resheba(self) -> None | str:
		async with aiohttp.ClientSession() as session:
			async with session.get(self.__subject_url, headers=config.HEADERS) as response:
				if response.status == 404:
					return None

				text = await response.text()
				soup = BeautifulSoup(text, 'html.parser')

				# Текст решения
				solution_text: list[str] = [p.getText() for p in soup.find_all('div', class_='taskText')]
				return ''.join(solution_text).replace('\n\n', '\n')


def get_title(book: str, numbering: str) -> str | None:
	subject = book.split()[0].lower()

	title_formats = {
		'английский': f'{book}, страница {numbering}',
		'русский': f'{book}, упражнение {numbering}',
		'алгебра-задачник': f'{book}, номер {numbering}',
		'геометрия': f'{book}, номер {numbering}',
		'обществознание': f'{book}, параграф §{numbering}'
		}

	return title_formats.get(subject, None)


async def send_solution(message: Message, solution: list[str] | str, title: str) -> None:
	if isinstance(solution, str):
		for text in split_text(solution):
			await message.answer(text)
	else:
		for url in solution:
			image = URLInputFile(url, filename=title)
			await bot.send_photo(chat_id=message.chat.id, photo=image)

			# Задержка после отправки, чтобы телеграм не выдавал ошибку
			await asyncio.sleep(config.MESSAGE_DELAY)

		await message.answer(title)


def split_text(text: str, max_length: int = 4096):
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


def get_subject_text(book: str) -> str:
	subject = book.split()[0].lower()

	subject_messages = {
		'английский': 'Теперь введи страницу 📖 _(от 10 до 180 включительно)_',
		'русский': 'Теперь введи упражнение 📃 _(от 1 до 396 включительно)_',
		'алгебра-задачник': 'Теперь введи номер задания 📖 _(от 1.1 до 60.19 включительно)_',
		'геометрия': 'Теперь введи номер задания 📖 _(от 1 до 870 включительно)_',
		'обществознание': ('Теперь введи параграф учебника 📖 _(от 1 до 44 включительно)_\n\nЕсли у вас параграф вида '
		                   '_"число-число"_, то просто введите число перед дефисом')
		}

	return subject_messages.get(subject, '')


def check_numbering(text: str) -> bool:
	if text.isnumeric() or re.match(config.ALGEBRA_NUMBER_PATTERN, text):
		return True
	return False
