from typing import Any

from aiogram.types import Message
from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.input import MessageInput

from app.parsers import ParseEnglish
from app.utils import send_solution


# async def get_book(manager: DialogManager):
# 	book = manager.dialog_data.get('book')
# 	return {'book': config.BOOKS.get(book)}


async def parse_page(message: Message, message_input: MessageInput, dialog_manager: DialogManager) -> None:
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
