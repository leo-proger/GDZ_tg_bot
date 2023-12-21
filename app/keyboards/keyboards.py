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

		# Добавляем последнюю кнопку в отдельный массив
		last_button = [
			InlineKeyboardButton(text=sections[0].capitalize(), callback_data='english-' + sections[0])]

		# Добавляем остальные кнопки в другой массив
		other_buttons = [InlineKeyboardButton(text=section.capitalize(), callback_data='english-' + section) for
		                 section in sections[1:]]

		builder.row(*other_buttons)
		builder.row(*last_button)
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
