import re

from .config import BOOKS
from .utils import get_annotation_text, PageParser


class BaseParser:
	def __init__(self, parse_url_base: str, book) -> None:
		self.parse_url_base = parse_url_base
		self.parse_url = None
		self.title = get_annotation_text(book=BOOKS.get(book)[0])

	async def get_solution_data(self):
		raise NotImplementedError("Метод должен быть переопределен в дочерних классах")


class ParseEnglish(BaseParser):
	def __init__(self, page: str = None, module: str = None, module_exercise: str = None,
	             spotlight_on_russia_page: str = None) -> None:
		super().__init__('https://gdz.ru/class-10/english/reshebnik-spotlight-10-afanaseva-o-v/', 'английский')

		self.page = page
		self.module = module
		self.module_exercise = module_exercise
		self.spotlight_on_russia_page = spotlight_on_russia_page

	async def get_solution_data(self):
		if self.page:
			self.parse_url = f'{self.page}-s/'
			self.title += get_annotation_text(раздел='страницы учебника', страница=self.page)
		elif self.module and self.module_exercise:
			self.parse_url = f'{int(self.module) + 1}-s-{self.module_exercise}/'
			self.title += get_annotation_text(раздел='Song Sheets', модуль=self.module, упражнение=self.module_exercise)
		elif self.spotlight_on_russia_page:
			self.parse_url = f'1-s-{self.spotlight_on_russia_page}/'
			self.title += get_annotation_text(раздел='Spotlight on Russia', страница=self.spotlight_on_russia_page)

		parser = PageParser(f'{self.parse_url_base}{self.parse_url}')
		result = await parser.parse_gdz()
		if not result:
			return None
		return {'solution': result, 'title': self.title}


class ParseRussian(BaseParser):
	def __init__(self, exercise: str = None) -> None:
		super().__init__('https://gdz.ru/class-10/russkii_yazik/vlasenkov-i-rybchenkova-10-11/', 'русский')
		self.exercise = exercise

	async def get_solution_data(self):
		if self.exercise:
			self.parse_url = f'{self.exercise}-nom/'
			self.title += get_annotation_text(упражнение=self.exercise)

		parser = PageParser(f'{self.parse_url_base}{self.parse_url}')
		result = await parser.parse_gdz()
		if not result:
			return None
		return {'solution': result, 'title': self.title}


class ParseMath(BaseParser):
	def __init__(self, number: str = None) -> None:
		super().__init__('https://gdz.ru/class-10/algebra/reshebnik-mordkovich-a-g/', 'алгебра-задачник')
		self.number = number.split('.') if number else None

	async def get_solution_data(self):
		if self.number:
			self.parse_url = f'{self.number[0]}-item-{self.number[1]}/'
			self.title += get_annotation_text(номер='.'.join(self.number))

		parser = PageParser(f'{self.parse_url_base}{self.parse_url}')
		result = await parser.parse_gdz()
		if not result:
			return None
		return {'solution': result, 'title': self.title}


class ParseGeometry(BaseParser):
	def __init__(self, number: str = None, chapter: str = None, page: str = None, exercise_to_page: str = None,
	             math_number: str = None, research_number: str = None) -> None:
		super().__init__('https://gdz.ru/class-10/geometria/atanasyan-10-11/', 'геометрия')
		self.number = number
		self.chapter = chapter
		self.page = page
		self.exercise_to_page = exercise_to_page
		self.math_number = math_number
		self.research_number = research_number

	async def get_solution_data(self):
		if self.number:
			class_type = '10' if self.number and int(self.number) < 400 else '11'
			self.parse_url = f'{class_type}-class-{self.number}/'
			self.title += get_annotation_text(номер=self.number)
		elif self.chapter:
			self.parse_url = f'vorosi-{self.chapter}/'
			self.title += get_annotation_text(глава=self.chapter)
		elif self.page and self.exercise_to_page:
			self.parse_url = f'ege-{self.page}-{self.exercise_to_page}/'
			self.title += get_annotation_text(страница=self.page, задача=self.exercise_to_page)
		elif self.math_number:
			self.parse_url = f'math-{self.math_number}/'
			self.title += get_annotation_text(задача=self.math_number)
		elif self.research_number:
			self.parse_url = f'res-{self.research_number}/'
			self.title += get_annotation_text(задача=self.research_number)

		parser = PageParser(f'{self.parse_url_base}{self.parse_url}')
		result = await parser.parse_gdz()
		if not result:
			return None
		return {'solution': result, 'title': self.title}


class ParseSociology(BaseParser):
	def __init__(self, paragraph: str = None) -> None:
		super().__init__('https://resheba.me/gdz/obshhestvoznanie/10-klass/soboleva/', 'обществознание')
		self.paragraph = paragraph

	async def get_solution_data(self):
		if self.paragraph:
			self.parse_url = f'paragraph-{self.paragraph}'
			self.title += get_annotation_text(параграф=self.paragraph)

		parser = PageParser(f'{self.parse_url_base}{self.parse_url}')
		result = await parser.parse_resheba()
		if not result:
			return None
		return {'solution': result, 'title': self.title}


class ParsePhysics(BaseParser):
	def __init__(self, paragraph: str = None, question: str = None, exercise: str = None) -> None:
		super().__init__('https://reshak.ru/', 'физика')
		self.paragraph = paragraph
		self.question = question
		self.exercise = exercise

	async def get_solution_data(self):
		if self.question:
			# Часть строки "otvet/reshebniki.php?" в parse_url_base не переносить, так как заденет другие части кода
			self.parse_url = f'otvet/reshebniki.php?otvet={self.paragraph}/{self.question}&predmet=myakishev10/'
			self.title += get_annotation_text(параграф=self.paragraph, вопрос=self.question)
		elif self.exercise:
			links = await self.find_list_exercises()
			self.parse_url = await self.get_final_link(links)
			self.title += get_annotation_text(параграф=self.paragraph, задание=self.exercise)

		parser = PageParser(f'{self.parse_url_base}{self.parse_url}')
		result = await parser.parse_reshak()
		if not result:
			return None
		return {'solution': result, 'title': self.title}

	async def find_list_exercises(self) -> list[str] or None:
		parse_url = 'https://reshak.ru/reshebniki/fizika/10/myakishev/index.html'
		soup = await PageParser.parse_page(parse_url)
		if not soup:
			return None

		element_subtitle = soup.find_all(
			lambda tag: tag.get('class') == ['subtitle'] and self.paragraph in tag.text)

		if element_subtitle:
			element_razdel = element_subtitle[0].find_next()
			links = [a.get('href') for a in element_razdel.find_all('a', href=True)]
			return links
		else:
			return None

	async def get_final_link(self, links: list[str]) -> str:
		for link in links:
			match = re.search(r'otvet=\d+/([a-c]\d)&predmet=myakishev10', link)
			if match:
				number = match.group(1)[1:]
				if self.exercise == number:
					return link
		return ''
