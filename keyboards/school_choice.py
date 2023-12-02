from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import config


def select_book_kb() -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()

	for book in config.BOOKS:
		builder.add(KeyboardButton(text=book))

	# builder.adjust(num) сколько кнопок будет по горизонтали
	return builder.as_markup(resize_keyboard=True)
