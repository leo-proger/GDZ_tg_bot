import re

import aiohttp
from bs4 import BeautifulSoup

from config import HEADERS, NUMBER_PATTERN


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


async def get_solve(book: str, page: str = None, exercise: str = None, number: str = None) -> dict:
	if number and not re.match(NUMBER_PATTERN, number):
		return {'text': 'Номер', 'ending': '', 'status_code': 404}

	subject_urls = {
		'английский': rf'https://gdz.ru/class-10/english/reshebnik-spotlight-10-afanaseva-o-v/{page}-s/',
		'русский': rf'https://gdz.ru/class-10/russkii_yazik/vlasenkov-i-rybchenkova-10-11/{exercise}-nom/',
		'алгебра-задачник': r'https://gdz.ru/class-10/algebra/reshebnik-mordkovich-a-g/{}-item-{}/'.format(
			*(number.split('.') if number else ['', '']), None)
		}
	subject = book.split()[0].lower()

	url = subject_urls.get(subject)
	if url is None:
		return {'status_code': 404}

	solutions_url = await parse_gdz(url)

	print(f'{page}, {exercise}, {number}')
	if solutions_url:
		title = ''
		if page is not None:
			title = f"{book}, страница {page}"
		elif exercise is not None:
			title = f"{book}, упражнение {exercise}"
		elif number is not None:
			title = f"{book}, номер {number}"

		return {'title': title, 'solutions_url': solutions_url, 'status_code': 200}

	text = ending = ''  # {text} не найден{ending}
	if page is not None:
		text, ending = 'Страница', 'а'
	elif exercise is not None:
		text, ending = 'Упражнение', 'о'
	elif number is not None:
		text, ending = 'Номер', ''

	return {'text': text, 'ending': ending, 'status_code': 404}

# dct = {
# 	'subject': SUBJECTS['with_pages'].get('english'),
# 	'page': 10434
# 	}
# print(get_solve(dct))
