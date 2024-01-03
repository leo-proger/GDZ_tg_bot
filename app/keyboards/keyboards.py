from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram_dialog.widgets.kbd import Start, Row, Select, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from app import config
from ..handlers.english import parse_module_exercise
from ..selected import save_module
from ..states import FormEnglish


def book_selection_kb() -> list[Start]:
	buttons = [Start(text=Const(book[0]), id=book[1].replace(' ', '_').lower(), state=book[2])
	           for book in config.BOOKS.values()]
	return buttons


class EnglishKeyboards:
	@staticmethod
	def section_selection_kb(book: str = 'английский spotlight 10 класс в. эванс, д. дули'):
		sections = config.SECTIONS.get(book.lower())

		btn1 = SwitchTo(Const(sections[0]), id='section1', state=FormEnglish.spotlight_on_russia_page)
		btn2 = SwitchTo(Const(sections[1]), id='section2', state=FormEnglish.module)
		btn3 = SwitchTo(Const(sections[2]), id='section3', state=FormEnglish.page)

		buttons = [Row(btn1, btn2), btn3]
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
		return [row_buttons1, row_buttons2]

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
	def section_selection_kb(book: str) -> InlineKeyboardMarkup:
		sections = config.SECTIONS.get(book.lower())
		builder = InlineKeyboardBuilder()

		for section in sections:
			builder.add(
				InlineKeyboardButton(
					text=section,
					callback_data='geometry_section-' + section
					)
				)
		builder.adjust(2)
		return builder.as_markup()

	@staticmethod
	def chapter_selection_kb() -> InlineKeyboardMarkup:
		builder = InlineKeyboardBuilder()

		for chapter in range(1, 7):
			builder.add(
				InlineKeyboardButton(
					text=str(chapter),
					callback_data='geometry_chapter-' + str(chapter)
					)
				)
		builder.adjust(3)
		return builder.as_markup()

	@staticmethod
	def page_selection_kb() -> InlineKeyboardMarkup:
		builder = InlineKeyboardBuilder()

		pages = [InlineKeyboardButton(text=str(page), callback_data=f'geometry_page-{page}') for page in
		         range(229, 236, 2)]
		builder.add(*pages)
		builder.add(InlineKeyboardButton(text='236', callback_data='geometry_page-236'))

		builder.adjust(3)
		return builder.as_markup()


class PhysicsKeyboards:
	@staticmethod
	def section_selection_kb(book: str) -> InlineKeyboardMarkup:
		sections = config.SECTIONS.get(book.lower())
		builder = InlineKeyboardBuilder()

		for section in sections:
			builder.add(
				InlineKeyboardButton(
					text=section,
					callback_data='physics_section-' + section
					)
				)
		builder.adjust(1)
		return builder.as_markup()
