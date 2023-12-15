import re

import aiohttp
from bs4 import BeautifulSoup

from app import config
from app.config import HEADERS, NUMBER_PATTERN


async def parse_resheba(url: str) -> None | str:
	async with aiohttp.ClientSession() as session:
		async with session.get(url, headers=HEADERS) as response:
			if response.status == 404:
				return None

			text = await response.text()
			soup = BeautifulSoup(text, 'html.parser')

			# Текст решения
			solution_text: list[str] = [p.getText() for p in soup.find_all('div', class_='taskText')]

			# return ''.join(solution_text).replace('<div class="taskText">', '').replace('</div>', '').replace('<p>',
			# '').replace('</p>', '').replace('<strong>', '**').replace( '</strong>', '**').strip().replace('\n\n',
			# '\n')
			return ''.join(solution_text).replace('\n\n', '\n')


async def parse_gdz(url: str) -> None | list[str]:
	async with aiohttp.ClientSession() as session:
		async with session.get(url, headers=HEADERS) as response:
			if response.status == 404:
				return None

			text = await response.text()
			soup = BeautifulSoup(text, 'html.parser')

			# Url фоток с решениями
			solutions_url: list[str] = ['https:' + div.img['src'] for div in
			                            soup.find_all('div', class_='with-overtask')]

			if not solutions_url:
				no_solution: list[str] = ['https://gdz.ru' + soup.find('div', class_='task-img-container').img['src']]
				return no_solution

			return solutions_url


async def get_solve(book: str, page: str = None, exercise: str = None, number: str = None,
                    paragraph: str = None) -> dict:
	if number and (book == config.BOOKS.get('алгебра-задачник')) and (not re.match(NUMBER_PATTERN, number)):
		return {'text': 'Номер', 'suffix': '', 'status_code': 404}

	subject_urls = {
		'английский': rf'https://gdz.ru/class-10/english/reshebnik-spotlight-10-afanaseva-o-v/{page}-s/',
		'русский': rf'https://gdz.ru/class-10/russkii_yazik/vlasenkov-i-rybchenkova-10-11/{exercise}-nom/',

		'алгебра-задачник': r'https://gdz.ru/class-10/algebra/reshebnik-mordkovich-a-g/{}-item-{}/'.format(
			*(number.split('.') if number else ['', '']), None),

		'геометрия': r'https://gdz.ru/class-10/geometria/atanasyan-10-11/{}-class-{}/'.format(
			'10' if number and '.' not in number and int(number) < 400 else '11', number
			),

		'обществознание': rf'https://resheba.me/gdz/obshhestvoznanie/10-klass/soboleva/paragraph-{paragraph}',
		}
	# Название предмета (русский, алгебра и тд)
	subject = book.split()[0].lower()

	solution_text = solutions_url = None

	url = subject_urls.get(subject)
	if url is None:
		return {'status_code': 404}

	if subject.lower() == 'обществознание':
		solution_text = await parse_resheba(url)
	else:
		solutions_url = await parse_gdz(url)

	if solutions_url:
		title = ''
		if page is not None:
			title = f"{book}, страница {page}"
		elif exercise is not None:
			title = f"{book}, упражнение {exercise}"
		elif number is not None:
			title = f"{book}, номер {number}"

		return {'title': title, 'solution': solutions_url, 'status_code': 200}
	elif solution_text:
		title = f'{book}, параграф §{paragraph}'
		return {'title': title, 'solution': solution_text, 'status_code': 200}

	text = suffix = ''  # {text} не найден{suffix}
	if page is not None:
		text, suffix = 'Страница', 'а'
	elif exercise is not None:
		text, suffix = 'Упражнение', 'о'
	elif number is not None:
		text, suffix = 'Номер', ''
	elif paragraph is not None:
		text, suffix = 'Параграф', ''

	return {'text': text, 'suffix': suffix, 'status_code': 404}

# dct = dict(
# 	book='Обществознание 10 Класс О.Б. Соболева, В.В. Барабанов',
# 	paragraph=1
# 	)
# solve = asyncio.run(get_solve(**dct)).get('solution')
# print(split_text(solve))
