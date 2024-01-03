from aiogram import F
from aiogram.types import ContentType, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const

from app import config
from app.handlers.english import parse_page, parse_spotlight_on_russia_page
from app.handlers.russian import parse_exercise
from app.keyboards.keyboards import book_selection_kb, EnglishKeyboards
from app.states import MainForm, FormEnglish, FormRussian, FormMath
from app.handlers.math import parse_number

kb_english = EnglishKeyboards()


async def other_type_handler(message: Message, message_input: MessageInput,
                             dialog_manager: DialogManager):
	await message.answer('Не найдено 😕')
	await dialog_manager.done()


main_dialog = Dialog(
	Window(
		Const('Выбери учебник 📐📓📊📘'),
		*book_selection_kb(),
		markup_factory=ReplyKeyboardFactory(
			input_field_placeholder=Const("Выбери учебник из списка ниже"),
			resize_keyboard=True,
			),
		state=MainForm.book
		)
	)

dialog_english = Dialog(
	Window(
		Const('Теперь выбери раздел учебника'),
		*kb_english.section_selection_kb(),
		state=FormEnglish.section
		),
	Window(
		Const('Теперь введи страницу учебника 📖 _(от 10 до 180 включительно)_'),
		MessageInput(parse_page, content_types=[ContentType.TEXT], filter=F.text.isdigit()),
		MessageInput(other_type_handler),
		state=FormEnglish.page
		),
	Window(
		Const('Теперь выбери страницу раздела 📖 _(от 2 до 10 включительно)_'),
		MessageInput(parse_spotlight_on_russia_page, content_types=[ContentType.TEXT], filter=F.text.isdigit()),
		MessageInput(other_type_handler),
		state=FormEnglish.spotlight_on_russia_page
		),
	Window(
		Const('Теперь выбери модуль 📖 _(от 1 до 8 включительно)_'),
		*kb_english.module_selection_kb(),
		MessageInput(parse_spotlight_on_russia_page, content_types=[ContentType.TEXT], filter=F.text.isdigit()),
		MessageInput(other_type_handler),
		state=FormEnglish.module
		),
	Window(
		Const('Осталось выбрать упражнение из модуля'),
		kb_english.module_exercise_selection_kb(),
		state=FormEnglish.module_exercise
		)
	)
dialog_russian = Dialog(
	Window(
		Const('Теперь введи упражнение 📃 _(от 1 до 396 включительно)_'),
		MessageInput(parse_exercise, content_types=[ContentType.TEXT], filter=F.text.isdigit()),
		MessageInput(other_type_handler),
		state=FormRussian.exercise
		)
	)
dialog_math = Dialog(
	Window(
		Const('Теперь введи номер задания 📖 _(от 1.1 до 60.19 включительно)_'),
		MessageInput(parse_number, content_types=[ContentType.TEXT],
		             filter=F.text.regexp(config.FLOAT_NUMBER_PATTERN)),
		MessageInput(other_type_handler),
		state=FormMath.number
		)
	)
