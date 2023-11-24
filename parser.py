import requests
from bs4 import BeautifulSoup

from config import SUBJECTS, HEADERS


def parse_gdz(url: str):
	request = requests.get(url, headers=HEADERS)
	if request.status_code == 404:
		return 404

	soup = BeautifulSoup(request.text, 'html.parser')

	# Url фото с решениями
	exercise_solutions = ['https:' + div.img['src'] for div in soup.find_all('div', class_='with-overtask')]

	return exercise_solutions


def get_solve(data: dict, pages: bool = True):
	if pages:
		subject = data.get('subject')
		if subject == SUBJECTS['with_pages'].get('english'):
			page = data.get('page')

			url = fr'https://gdz.ru/class-10/english/reshebnik-spotlight-10-afanaseva-o-v/{page}-s/'

			# В атрибуте src неполная ссылку
			parsed_solutions = parse_gdz(url)
			if parsed_solutions != 404:
				title = f"{SUBJECTS['with_pages'].get('english')} страница {page}"

				return {'solutions': parsed_solutions, 'title': title, 'status_code': 200}
			else:
				return {'status_code': 404}


# dct = {
# 	'subject': SUBJECTS['with_pages'].get('english'),
# 	'page': 10434
# 	}
# print(get_solve(dct))
