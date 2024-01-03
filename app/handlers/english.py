from typing import Any

from aiogram import Router
from aiogram.types import Message
from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.input import MessageInput

from app.parsers import ParseEnglish
from app.utils import send_solution

router_english = Router()


# async def get_book(manager: DialogManager):
# 	book = manager.dialog_data.get('book')
# 	return {'book': config.BOOKS.get(book)}


async def parse_page(message: Message, message_input: MessageInput, dialog_manager: DialogManager) -> None:
	# ic(message)
	# ic(message_input)
	# ic(dialog_manager)
	dialog_manager.dialog_data['page'] = message.text

	parser = ParseEnglish(page=message.text)
	result = await parser.get_solution_data()

	await send_solution(message, result, dialog_manager)


async def parse_spotlight_on_russia_page(message: Message, message_input: MessageInput,
                                         dialog_manager: DialogManager) -> None:
	dialog_manager.dialog_data['spotlight_on_russia_page'] = message.text

	parser = ParseEnglish(spotlight_on_russia_page=message.text)
	result = await parser.get_solution_data()

	await send_solution(message, result, dialog_manager)


async def parse_module_exercise(callback: ChatEvent, select: Any,
                                dialog_manager: DialogManager,
                                item_id: str) -> None:
	module = dialog_manager.dialog_data.get('module', '0')

	parser = ParseEnglish(module=module, module_exercise=item_id)
	result = await parser.get_solution_data()

	await send_solution(callback.message, result, dialog_manager)

# @router_english.callback_query(F.data.startswith('english_module-'))
# async def module_selection(callback: CallbackQuery, state: FSMContext) -> None:
# 	module = callback.data.split('-')[1]
# 	await state.update_data(module=module)
#
# 	await callback.message.edit_text('Осталось выбрать упражнение из модуля',
# 	                                 reply_markup=kb_english.module_exercise_selection_kb())
# 	await callback.answer()


# @router_english.callback_query(F.data.startswith('english-'))
# async def section_selection(callback: CallbackQuery, dialog_manager: DialogManager) -> None:
# 	section = callback.data.split('-')[1]
#
# 	if section == 'Страницы учебника':
# 		await dialog_manager.start(FormEnglish.page)
# 	# await state.set_state(FormEnglish.page)
# 	# await callback.message.edit_text('Теперь выбери страницу учебника 📖 _(от 10 до 180 включительно)_',
# 	#                                  reply_markup=None)
# 	elif section == 'Spotlight on Russia':
# 		await state.set_state(FormEnglish.spotlight_on_russia_page)
# 		await callback.message.edit_text('Теперь выбери страницу раздела 📖 _(от 2 до 10 включительно)_',
# 		                                 reply_markup=None)
# 	elif section == 'Song sheets':
# 		await state.set_state(FormEnglish.module)
# 		await callback.message.edit_text('Теперь выбери модуль 📖 _(от 1 до 8 включительно)_',
# 		                                 reply_markup=kb_english.module_selection_kb())
# 	await callback.answer()
