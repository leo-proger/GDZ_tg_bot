from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram_dialog.widgets.kbd import Start, Row, Select, Column, Button, SwitchTo
from aiogram_dialog.widgets.text import Const, Format

from app import config
from ..states import FormEnglish


def book_selection_kb() -> list[Start]:
	buttons = [Start(text=Const(book[0]), id=book[1].replace(' ', '_').lower(), state=book[2])
	           for book in config.BOOKS.values()]
	return buttons


class EnglishKeyboards:
	@staticmethod
	def section_selection_kb(book: str = 'английский spotlight 10 класс в. эванс, д. дули'):
		sections = config.SECTIONS.get(book.lower())
		# buttons = Column(Select(
		# 	Format('{item}'),
		# 	items=sections,
		# 	item_id_getter=lambda x: x.replace(' ', '_').lower(),
		# 	id='section_selection',
		# 	on_click=selected.english_check_section
		# 	))
		btn1 = Button(text=Const(sections[0]), id='section1')
		btn2 = Button(text=Const(sections[1]), id='section2')
		btn3 = SwitchTo(Const(sections[2]), id='section3', state=FormEnglish.page)
		buttons = [Row(btn1, btn2), btn3]
		return buttons

	@staticmethod
	def module_selection_kb() -> InlineKeyboardMarkup:
		builder = InlineKeyboardBuilder()

		for module in range(1, 9):
			builder.add(
				InlineKeyboardButton(
					text=str(module),
					callback_data='english_module-' + str(module)
					)
				)
		builder.adjust(4)
		return builder.as_markup()

	@staticmethod
	def module_exercise_selection_kb() -> InlineKeyboardMarkup:
		builder = InlineKeyboardBuilder()

		for exercise in range(1, 5):
			builder.add(
				InlineKeyboardButton(
					text=str(exercise),
					callback_data='english_module_exercise-' + str(exercise)
					)
				)
		builder.adjust(2)
		return builder.as_markup()


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
