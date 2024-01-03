from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType
from aiogram_dialog import Window, Dialog, DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const
from icecream import ic

from app.keyboards.keyboards import EnglishKeyboards
# from app.keyboards.keyboards import EnglishKeyboards, book_selection_kb
from app.parsers import ParseEnglish
from app.states import FormEnglish
from app.utils import send_solution

router_english = Router()

kb_english = EnglishKeyboards()


# async def get_book(manager: DialogManager):
# 	book = manager.dialog_data.get('book')
# 	return {'book': config.BOOKS.get(book)}


# @router_english.message(FormEnglish.page)
async def parse_page(message: Message, message_input: MessageInput, dialog_manager: DialogManager) -> None:
	# ic(message)
	# ic(message_input)
	# ic(dialog_manager)
	if message.text.isnumeric():
		dialog_manager.dialog_data['page'] = message.text

		parser = ParseEnglish(page=message.text)
		result = await parser.get_solution_data()

		await send_solution(message, result, dialog_manager)
	else:
		await message.answer('Не найдено 😕')
		await dialog_manager.done()


# @router_english.message(FormEnglish.spotlight_on_russia_page)
async def parse_spotlight_on_russia_page(message: Message, state: FSMContext) -> None:
	if message.text.isnumeric():
		await state.update_data(spotlight_on_russia_page=message.text)

		parser = ParseEnglish(spotlight_on_russia_page=message.text)
		result = await parser.get_solution_data()

		await send_solution(message, result, state)
	else:
		await message.answer('Не найдено 😕', reply_markup=book_selection_kb())
		await state.clear()





# @router_english.callback_query(F.data.startswith('english_module_exercise-'))
# async def parse_module_exercise(callback: CallbackQuery, state: FSMContext) -> None:
# 	data = await state.get_data()
# 	module_exercise = callback.data.split('-')[1]
#
# 	parser = ParseEnglish(module=data.get('module'), module_exercise=module_exercise)
# 	result = await parser.get_solution_data()
#
# 	await send_solution(callback.message, result, state)
# 	await callback.answer()
#
#
# @router_english.callback_query(F.data.startswith('english_module-'))
# async def module_selection(callback: CallbackQuery, state: FSMContext) -> None:
# 	module = callback.data.split('-')[1]
# 	await state.update_data(module=module)
#
# 	await callback.message.edit_text('Осталось выбрать упражнение из модуля',
# 	                                 reply_markup=kb_english.module_exercise_selection_kb())
# 	await callback.answer()


@router_english.callback_query(F.data.startswith('english-'))
async def section_selection(callback: CallbackQuery, dialog_manager: DialogManager) -> None:
	section = callback.data.split('-')[1]

	if section == 'Страницы учебника':
		await dialog_manager.start(FormEnglish.page)
	# await state.set_state(FormEnglish.page)
	# await callback.message.edit_text('Теперь выбери страницу учебника 📖 _(от 10 до 180 включительно)_',
	#                                  reply_markup=None)
	elif section == 'Spotlight on Russia':
		await state.set_state(FormEnglish.spotlight_on_russia_page)
		await callback.message.edit_text('Теперь выбери страницу раздела 📖 _(от 2 до 10 включительно)_',
		                                 reply_markup=None)
	elif section == 'Song sheets':
		await state.set_state(FormEnglish.module)
		await callback.message.edit_text('Теперь выбери модуль 📖 _(от 1 до 8 включительно)_',
		                                 reply_markup=kb_english.module_selection_kb())
	await callback.answer()
