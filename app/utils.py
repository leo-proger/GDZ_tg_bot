import asyncio
import re

import aiohttp
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile
from bs4 import BeautifulSoup

from app import config
from app.keyboards.keyboards import book_selection_kb
from main import bot


# class Parser:
# 	def __init__(self, book: str, numbering: str) -> None:
# 		self.book = book
# 		self.numbering = numbering
#
# 		self.__subject_url = ''
# 		self.__parser_engine = config.PARSER_ENGINE
#
# 	async def get_solution_data(self) -> None | dict[str, str]:
# 		subject = self.book.split()[0].lower()
#
# 		if subject == 'английский':
# 			self.__subject_url = rf'https://gdz.ru/class-10/english/reshebnik-spotlight-10-afanaseva-o-v/{self.numbering}-s/'
# 		elif subject == 'русский':
# 			self.__subject_url = rf'https://gdz.ru/class-10/russkii_yazik/vlasenkov-i-rybchenkova-10-11/{self.numbering}-nom/'
# 		elif subject == 'алгебра-задачник' and re.match(config.ALGEBRA_NUMBER_PATTERN, self.numbering):
# 			parts_of_number = self.numbering.split('.')
# 			self.__subject_url = (
# 				rf'https://gdz.ru/class-10/algebra/reshebnik-mordkovich-a-g/{parts_of_number[0]}-item-'
# 				rf'{parts_of_number[1]}/')
# 		elif subject == 'геометрия':
# 			class_number = '10' if int(self.numbering) < 400 else '11'
# 			self.__subject_url = rf'https://gdz.ru/class-10/geometria/atanasyan-10-11/{class_number}-class-{self.numbering}/'
# 		elif subject == 'обществознание':
# 			self.__subject_url = rf'https://resheba.me/gdz/obshhestvoznanie/10-klass/soboleva/paragraph-{self.numbering}'
# 			self.__parser_engine = 'resheba.ru'
# 		else:
# 			return None
#
# 		result = await self.__parse_solution()
# 		if result:
# 			return {'solution': result, 'title': get_title(self.book, self.numbering)}
# 		return None
#
# 	async def __parse_solution(self) -> list[str] | str | None:
# 		"""Значения, которые может вернуть метод
# 			list[str]: Решение в виде фотографий с сайта gdz.ru
# 			str: Решение обществознания, которое берется с сайта resheba.ru
# 			"""
# 		if self.__subject_url:
# 			if self.__parser_engine == 'gdz.ru':
# 				return await self.__parse_gdz()
# 			elif self.__parser_engine == 'resheba.ru':
# 				return await self.__parse_resheba()
#
# 	async def __parse_gdz(self) -> None | list[str]:
# 		async with aiohttp.ClientSession() as session:
# 			async with session.get(self.__subject_url, headers=config.HEADERS) as response:
# 				if response.status == 404:
# 					return None
#
# 				text = await response.text()
# 				soup = BeautifulSoup(text, 'html.parser')
#
# 				# Url фоток с решениями
# 				solutions_url: list[str] = ['https:' + div.img['src'] for div in
# 				                            soup.find_all('div', class_='with-overtask')]
#
# 				if not solutions_url:
# 					no_solution: list[str] = [
# 						'https://gdz.ru' + soup.find('div', class_='task-img-container').img['src']]
# 					return no_solution
#
# 				return solutions_url
#
# 	async def __parse_resheba(self) -> None | str:
# 		async with aiohttp.ClientSession() as session:
# 			async with session.get(self.__subject_url, headers=config.HEADERS) as response:
# 				if response.status == 404:
# 					return None
#
# 				text = await response.text()
# 				soup = BeautifulSoup(text, 'html.parser')
#
# 				# Текст решения
# 				solution_text: list[str] = [p.getText() for p in soup.find_all('div', class_='taskText')]
# 				return ''.join(solution_text).replace('\n\n', '\n')


async def send_solution(message: Message, result: dict | None, state: FSMContext) -> None:
	if not result:
		await message.answer('Не найдено 😕', reply_markup=book_selection_kb())
		await state.clear()
	else:
		solution, title = result.get('solution'), result.get('title')
		if isinstance(solution, str):
			for text in split_text(solution):
				await message.answer(text)
				await asyncio.sleep(config.MESSAGE_DELAY)
		elif isinstance(solution, list):
			for url in solution:
				if url.startswith('https://'):
					image = URLInputFile(url, filename=title)
					await bot.send_photo(chat_id=message.chat.id, photo=image)
				else:
					await message.answer(url)

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


async def parse_gdz(parse_url) -> None | list[str]:
	async with aiohttp.ClientSession() as session:
		async with session.get(parse_url, headers=config.HEADERS) as response:
			if response.status == 404:
				return None

			page = await response.text()
			# TODO: Попробовать сделать асинхронным
			soup = BeautifulSoup(page, 'html.parser')

			# Url фоток с решениями
			solutions_url: list[str] = ['https:' + div.img['src'] for div in
			                            soup.find_all('div', class_='with-overtask')]

			if not solutions_url:
				no_solution: list[str] = [
					'https://gdz.ru' + soup.find('div', class_='task-img-container').img['src']]
				return no_solution

			return solutions_url


async def parse_resheba(parse_url) -> None | str:
	async with aiohttp.ClientSession() as session:
		async with session.get(parse_url, headers=config.HEADERS) as response:
			if response.status == 404:
				return None

			page = await response.text()
			soup = BeautifulSoup(page, 'html.parser')

			# Текст решения
			solution_text: list[str] = [p.getText() for p in soup.find_all('div', class_='taskText')]
			return ''.join(solution_text).replace('\n\n', '\n')


async def parse_reshak(parse_url) -> None | list[str]:
	async with aiohttp.ClientSession() as session:
		async with session.get(parse_url, headers=config.HEADERS) as response:
			if response.status == 404:
				return None

			page = await response.text()
			soup = BeautifulSoup(page, 'html.parser')
			result = []

			for el in soup.find_all('h2', class_='titleh2'):
				result.append(el.get_text())
				img_link = el.find_next('div').img.get('src', '')
				if not img_link:
					img_link = el.find_next('div').img.get('data-src', '')
				result.append('https://reshak.ru/' + img_link)
			return result


class ParseEnglish:
	def __init__(self, page: str = None, module: str = None, module_exercise: str = None,
	             spotlight_on_russia_page: str = None) -> None:
		self.page = page
		self.module = module
		self.module_exercise = module_exercise
		self.spotlight_on_russia_page = spotlight_on_russia_page

		self.__parse_url = 'https://gdz.ru/class-10/'
		self.__title = ''
		self.__parser_engine = config.PARSER_ENGINE

	async def get_solution_data(self) -> None | dict:
		if self.page:
			self.__parse_url += rf'english/reshebnik-spotlight-10-afanaseva-o-v/{self.page}-s/'
			self.__title = config.TITLE_MESSAGE + (f'Учебник: ***{config.BOOKS.get("английский")}***\n'
			                                       f'Раздел: ***Страницы учебника***\n'
			                                       f'Страница: ***{self.page}***')
		elif self.module and self.module_exercise:
			self.__parse_url += (
				rf'english/reshebnik-spotlight-10-afanaseva-o-v/{int(self.module) + 1}-s-{self.module_exercise}/')
			self.__title = config.TITLE_MESSAGE + (f'Учебник: ***{config.BOOKS.get("английский")}***\n'
			                                       f'Раздел: ***Song Sheets***\n'
			                                       f'Модуль: ***{self.module}***\n'
			                                       f'Упражнение: ***{self.module_exercise}***')
		elif self.spotlight_on_russia_page:
			self.__parse_url += rf'english/reshebnik-spotlight-10-afanaseva-o-v/1-s-{self.spotlight_on_russia_page}/'
			self.__title = config.TITLE_MESSAGE + (f'Учебник: ***{config.BOOKS.get("английский")}***\n'
			                                       f'Раздел: ***Spotlight on Russia***\n'
			                                       f'Страница: ***{self.spotlight_on_russia_page}***')

		result = await parse_gdz(self.__parse_url)
		if not result:
			return None
		return {'solution': result, 'title': self.__title}


class ParseRussian:
	def __init__(self, exercise: str = None) -> None:
		self.exercise = exercise

		self.__parse_url = 'https://gdz.ru/class-10/'
		self.__title = ''

	async def get_solution_data(self):
		if self.exercise:
			self.__parse_url += rf'russkii_yazik/vlasenkov-i-rybchenkova-10-11/{self.exercise}-nom/'
			self.__title = config.TITLE_MESSAGE + (f'Учебник: ***{config.BOOKS.get("русский")}***\n'
			                                       f'Упражнение: ***{self.exercise}***')
		result = await parse_gdz(self.__parse_url)
		if not result:
			return None
		return {'solution': result, 'title': self.__title}


class ParseMath:
	def __init__(self, number: str = None) -> None:
		self.number: list = number.split('.')

		self.__parse_url = 'https://gdz.ru/class-10/'
		self.__title = ''

	async def get_solution_data(self):
		if self.number:
			self.__parse_url += rf'algebra/reshebnik-mordkovich-a-g/{self.number[0]}-item-{self.number[1]}/'
			self.__title = config.TITLE_MESSAGE + (f'Учебник: ***{config.BOOKS.get("алгебра-задачник")}***\n'
			                                       f'Номер: ***{".".join(self.number)}***')

		result = await parse_gdz(self.__parse_url)
		if not result:
			return None
		return {'solution': result, 'title': self.__title}


class ParseGeometry:
	def __init__(self, number: str = None, chapter: str = None, page: str = None, exercise_to_page: str = None,
	             math_number: str = None, research_number: str = None) -> None:
		self.number = number
		self.chapter = chapter
		self.page = page
		self.exercise_to_page = exercise_to_page
		self.math_number = math_number
		self.research_number = research_number

		self.__class = '10' if number and int(number) < 400 else '11'
		self.__parse_url = 'https://gdz.ru/class-10/'
		self.__title = ''

	async def get_solution_data(self):
		if self.number:
			self.__parse_url += rf'geometria/atanasyan-10-11/{self.__class}-class-{self.number}/'
			self.__title = config.TITLE_MESSAGE + (f'Учебник: ***{config.BOOKS.get("геометрия")}***\n'
			                                       f'Номер: ***{self.number}***')
		elif self.chapter:
			self.__parse_url += rf'geometria/atanasyan-10-11/vorosi-{self.chapter}/'
			self.__title = config.TITLE_MESSAGE + (f'Учебник: ***{config.BOOKS.get("геометрия")}***\n'
			                                       f'Глава: ***{self.chapter}***')
		elif self.page and self.exercise_to_page:
			self.__parse_url += rf'geometria/atanasyan-10-11/ege-{self.page}-{self.exercise_to_page}/'
			self.__title = config.TITLE_MESSAGE + (f'Учебник: ***{config.BOOKS.get("геометрия")}***\n'
			                                       f'Страница: ***{self.page}***\n'
			                                       f'Задача: ***{self.exercise_to_page}***')
		elif self.math_number:
			self.__parse_url += rf'geometria/atanasyan-10-11/math-{self.math_number}/'
			self.__title = config.TITLE_MESSAGE + (f'Учебник: ***{config.BOOKS.get("геометрия")}***\n'
			                                       f'Задача: ***{self.math_number}***')
		elif self.research_number:
			self.__parse_url += rf'geometria/atanasyan-10-11/res-{self.research_number}/'
			self.__title = config.TITLE_MESSAGE + (f'Учебник: ***{config.BOOKS.get("геометрия")}***\n'
			                                       f'Задача: ***{self.research_number}***')
		result = await parse_gdz(self.__parse_url)
		if not result:
			return None
		return {'solution': result, 'title': self.__title}


class ParseSociology:
	def __init__(self, paragraph: str = None) -> None:
		self.paragraph = paragraph

		self.__parse_url = 'https://resheba.me/gdz/'
		self.__title = ''

	async def get_solution_data(self):
		if self.paragraph:
			self.__parse_url += rf'obshhestvoznanie/10-klass/soboleva/paragraph-{self.paragraph}'
			self.__title = config.TITLE_MESSAGE + (f'Учебник: ***{config.BOOKS.get("обществознание")}***\n'
			                                       f'Параграф: ***{self.paragraph}***')
		result = await parse_resheba(self.__parse_url)
		if not result:
			return None
		return {'solution': result, 'title': self.__title}


class ParsePhysics:
	def __init__(self, paragraph: str = None, question: str = None, exercise: str = None) -> None:
		self.paragraph = paragraph
		self.question = question
		self.exercise = exercise

		self.__parse_url = 'https://reshak.ru/'
		self.__title = ''

	async def get_solution_data(self):
		if self.question:
			self.__parse_url += rf'otvet/reshebniki.php?otvet={self.paragraph}/{self.question}&predmet=myakishev10/'
			self.__title = config.TITLE_MESSAGE + (f'Учебник: ***{config.BOOKS.get("физика")}***\n'
			                                       f'Параграф: ***{self.paragraph}***\n'
			                                       f'Вопрос: ***{self.question}***')
		elif self.exercise:
			links = await self.__find_list_exercises()
			if not links:
				return None
			self.__parse_url += await self.__get_final_link(links)
			self.__title = config.TITLE_MESSAGE + (f'Учебник: ***{config.BOOKS.get("физика")}***\n'
			                                       f'Параграф: ***{self.paragraph}***\n'
			                                       f'Задание: ***{self.exercise}***')
		result = await parse_reshak(self.__parse_url)
		if not result:
			return None
		return {'solution': result, 'title': self.__title}

	async def __find_list_exercises(self) -> list[str] | None:
		parse_url = 'https://reshak.ru/reshebniki/fizika/10/myakishev/index.html'

		async with aiohttp.ClientSession() as session:
			async with session.get(parse_url, headers=config.HEADERS) as response:
				if response.status == 404:
					return None

				text = await response.text()
				soup = BeautifulSoup(text, 'html.parser')

				element_subtitle = soup.find_all(
					lambda tag: tag.get('class') == ['subtitle'] and self.paragraph in tag.text)

				if element_subtitle:
					element_razdel = element_subtitle[0].find_next()
					links = [a.get('href') for a in element_razdel.find_all('a', href=True)]
					return links
				else:
					return None

	async def __get_final_link(self, links: list[str]) -> str:
		for link in links:
			match = re.search(r'otvet=\d+/([a-c]\d)&predmet=myakishev10', link)
			if match:
				number = match.group(1)[1:]  # Получение числа, следующего после буквы a, b или c
				if self.exercise == number:
					return link
		return ''
