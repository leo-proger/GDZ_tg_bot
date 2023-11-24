from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

import config


def choice_subject_kb() -> ReplyKeyboardMarkup:
	builder = ReplyKeyboardBuilder()

	for subject in config.SUBJECTS['with_pages'].values():
		builder.add(KeyboardButton(text=subject))

	# builder.adjust(num)
	return builder.as_markup(resize_keyboard=True)
