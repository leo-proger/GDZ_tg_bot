from aiogram_dialog.widgets.kbd import Start, Row, Select, SwitchTo, Button
from aiogram_dialog.widgets.text import Const, Format

from app import config
from ..handlers.english import parse_module_exercise
from ..handlers.geometry import parse_chapter, parse_research_exercise
from ..selected import save_module, save_page_for_exam_preparation_exercises
from ..states import FormEnglish, FormGeometry, FormPhysics
from ..utils import send_whats_new


def book_selection_kb() -> list[Start]:
	buttons = [Start(text=Const(book[0]), id=book[1].replace(' ', '_').lower(), state=book[2])
	           for book in config.BOOKS.values()]
	return buttons


def admin_actions_kb():
	btn1 = Button(text=Const('Разослать сообщение об обновлении'), id='mailing', on_click=send_whats_new)
	actions = [btn1]
	return actions


class EnglishKeyboards:
	@staticmethod
	def section_selection_kb(book: str = 'английский spotlight 10 класс в. эванс, д. дули') -> list[Row]:
		sections = config.SECTIONS.get(book.lower())

		btn1 = SwitchTo(Const(sections[0]), id='section1', state=FormEnglish.spotlight_on_russia_page)
		btn2 = SwitchTo(Const(sections[1]), id='section2', state=FormEnglish.module)
		btn3 = SwitchTo(Const(sections[2]), id='section3', state=FormEnglish.page)

		buttons = [Row(btn1, btn2), Row(btn3)]
		return buttons

	@staticmethod
	def module_selection_kb() -> list[Row]:
		row_buttons1 = Row(Select(
			text=Format('{item}'),
			id='module_selection_row1',
			item_id_getter=lambda item: item,
			items=range(1, 5),
			on_click=save_module
			))
		row_buttons2 = Row(Select(
			text=Format('{item}'),
			id='module_selection_row2',
			item_id_getter=lambda item: item,
			items=range(5, 9),
			on_click=save_module
			))
		buttons = [row_buttons1, row_buttons2]
		return buttons

	@staticmethod
	def module_exercise_selection_kb() -> Row:
		row_buttons = Row(Select(
			text=Format('{item}'),
			id='module_exercise_selection_row',
			item_id_getter=lambda item: item,
			items=range(1, 5),
			on_click=parse_module_exercise
			))
		return row_buttons


class GeometryKeyboards:
	@staticmethod
	def section_selection_kb(book: str = 'геометрия 10-11 класс л.с. атанасян, в.ф бутузов') -> list[Row]:
		sections = config.SECTIONS.get(book.lower())
		row1 = Row(
			SwitchTo(text=Const(sections[0]), id='section1', state=FormGeometry.chapter),
			SwitchTo(text=Const(sections[1]), id='section2', state=FormGeometry.page_for_exam_preparation_exercises)
			)
		row2 = Row(
			SwitchTo(text=Const(sections[2]), id='section3', state=FormGeometry.math_exercise),
			SwitchTo(text=Const(sections[3]), id='section4', state=FormGeometry.research_exercise)
			)
		row3 = Row(
			SwitchTo(text=Const(sections[4]), id='section5', state=FormGeometry.number)
			)
		buttons = [row1, row2, row3]
		return buttons

	@staticmethod
	def chapter_selection_kb() -> list[Row]:
		row1 = Row(Select(
			text=Format('{item}'),
			id='chapter_selection_row1',
			item_id_getter=lambda item: item,
			items=range(1, 5),
			on_click=parse_chapter
			))
		row2 = Row(Select(
			text=Format('{item}'),
			id='chapter_selection_row2',
			item_id_getter=lambda item: item,
			items=range(5, 8),
			on_click=parse_chapter
			))
		buttons = [row1, row2]
		return buttons

	@staticmethod
	def page_for_exam_preparation_exercises_selection_kb() -> list[Row]:
		row1 = Row(Select(
			text=Format('{item}'),
			id='page_for_exam_preparation_exercises_selection_row1',
			item_id_getter=lambda item: item,
			items=range(229, 236, 2),
			on_click=save_page_for_exam_preparation_exercises
			))
		row2 = Row(Select(
			text=Format('{item}'),
			id='page_for_exam_preparation_exercises_selection_row2',
			item_id_getter=lambda item: item,
			items=range(235, 237),
			on_click=save_page_for_exam_preparation_exercises
			))
		buttons = [row1, row2]
		return buttons

	@staticmethod
	def research_exercise_selection_kb() -> list[Row]:
		row1 = Row(Select(
			text=Format('{item}'),
			id='research_exercise_selection_row1',
			item_id_getter=lambda item: item,
			items=range(1, 4),
			on_click=parse_research_exercise
			))
		row2 = Row(Select(
			text=Format('{item}'),
			id='research_exercise_selection_row2',
			item_id_getter=lambda item: item,
			items=range(4, 6),
			on_click=parse_research_exercise
			))
		buttons = [row1, row2]
		return buttons


class PhysicsKeyboards:
	@staticmethod
	def section_selection_kb(book: str = 'физика 10 класс г.я. мякишев, б.б. буховцев') -> list[Row]:
		sections = config.SECTIONS.get(book.lower())

		row1 = Row(
			SwitchTo(Const(sections[0]), id='section1', state=FormPhysics.exercise)
			)
		row2 = Row(
			SwitchTo(Const(sections[1]), id='section2', state=FormPhysics.question)
			)
		buttons = [row1, row2]
		return buttons
