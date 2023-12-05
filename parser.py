from bs4 import BeautifulSoup
import aiohttp

from config import HEADERS


async def parse_gdz(url: str) -> int | list[str]:
	async with aiohttp.ClientSession() as session:
		async with session.get(url, headers=HEADERS) as response:
			if response.status == 404:
				return 404

			text = await response.text()
			soup = BeautifulSoup(text, 'html.parser')

			# TODO: Обработка ситуаций, когда "номер отсутствует" в гдз

			# Url фоток с решениями
			solutions_url: list[str] = ['https:' + div.img['src'] for div in
			                            soup.find_all('div', class_='with-overtask')]

			return solutions_url


async def get_solve(book: str, page_or_exercise: int) -> dict:
	subject_urls = {
		'английский': rf'https://gdz.ru/class-10/english/reshebnik-spotlight-10-afanaseva-o-v/{page_or_exercise}-s/',
		'русский': rf'https://gdz.ru/class-10/russkii_yazik/vlasenkov-i-rybchenkova-10-11/{page_or_exercise}-nom/',
		}
	subject = book.split()[0].lower()

	url = subject_urls.get(subject)
	if url is None:
		return {'status_code': 404}

	solutions_url = await parse_gdz(url)

	if isinstance(solutions_url, list):
		title = f"***{book}***, страница/упражнение ***{page_or_exercise}***"
		return {'title': title, 'solutions_url': solutions_url, 'status_code': 200}

	return {'status_code': 404}

# dct = {
# 	'subject': SUBJECTS['with_pages'].get('english'),
# 	'page': 10434
# 	}
# print(get_solve(dct))
