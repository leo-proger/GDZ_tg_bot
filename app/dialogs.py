from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Row, Button
from aiogram_dialog.widgets.markup.reply_keyboard import ReplyKeyboardFactory
from aiogram_dialog.widgets.text import Const

from app.handlers.english import parse_page
from app.keyboards.keyboards import book_selection_kb, EnglishKeyboards
from app.states import MainForm, FormEnglish
from aiogram.types import ContentType

kb_english = EnglishKeyboards()

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
		MessageInput(parse_page, content_types=[ContentType.TEXT]),
		state=FormEnglish.page
		),
	# Window(
	# 	Select(
	# 		Format('{book}'),
	# 		id='books',
	# 		items='book',
	# 		item_id_getter=lambda item: item
	# 		),
	# 	Const('Теперь выбери раздел учебника'),
	# 	state=FormEnglish.section,
	# 	getter=get_book,
	# 	),
	)