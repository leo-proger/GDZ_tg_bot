from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import config


def select_textbook_series_kb(subject) -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()

	for textbook in config.SUBJECTS['with_pages'][subject]:
		builder.add(KeyboardButton(text=textbook.title()))

	return builder.as_markup(resize_keyboard=True)


def select_subject_kb() -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()

	for subject in config.SUBJECTS['with_pages']:
		builder.add(KeyboardButton(text=subject.capitalize()))

	# builder.adjust(num) сколько кнопок будет по горизонтали
	return builder.as_markup(resize_keyboard=True)
