from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app import config


def book_selection_kb() -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()

	for book in config.BOOKS.values():
		builder.add(KeyboardButton(text=book))

	builder.adjust(1)  # Сколько кнопок будет по горизонтали
	return builder.as_markup(resize_keyboard=True)


class EnglishKeyboards:
	@staticmethod
	def section_selection_kb(book: str) -> InlineKeyboardMarkup:
		sections = config.SECTIONS.get(book.lower())
		builder = InlineKeyboardBuilder()

		sections_buttons = [InlineKeyboardButton(text=section, callback_data=f'english-{section}') for section in
		                    sections]

		builder.add(*sections_buttons)
		builder.adjust(2)
		return builder.as_markup()

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
