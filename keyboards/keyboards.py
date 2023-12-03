from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import config


def book_selection_kb() -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()

	for book in config.BOOKS.values():
		builder.add(KeyboardButton(text=book))

	builder.adjust(1)  # Сколько кнопок будет по горизонтали
	return builder.as_markup(resize_keyboard=True)
