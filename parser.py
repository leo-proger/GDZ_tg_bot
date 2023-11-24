import requests
from bs4 import BeautifulSoup

from config import HEADERS


def parse_gdz(url: str) -> list[str] | int:
	request = requests.get(url, headers=HEADERS)
	if request.status_code == 404:
		return 404

	soup = BeautifulSoup(request.text, 'html.parser')

	# Url фото с решениями
	exercise_solutions: list[str] = ['https:' + div.img['src'] for div in soup.find_all('div', class_='with-overtask')]

	return exercise_solutions


def get_solve(subject: str, textbook_series: str, page: int, pages: bool = True) -> dict:
	if pages:
		if subject.lower() == 'английский':
			url = rf'https://gdz.ru/class-10/english/reshebnik-spotlight-10-afanaseva-o-v/{page}-s/'

			parsed_solutions = parse_gdz(url)
			if parsed_solutions and parsed_solutions != 404:
				title = f"Английский {textbook_series} страница {page}"

				return {'solutions': parsed_solutions, 'title': title, 'status_code': 200}
			else:
				return {'status_code': 404}
	return {'status_code': 500}

# dct = {
# 	'subject': SUBJECTS['with_pages'].get('english'),
# 	'page': 10434
# 	}
# print(get_solve(dct))
