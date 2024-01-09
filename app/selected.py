from typing import Any

from aiogram.types import Message
from aiogram_dialog import ChatEvent, DialogManager
from aiogram_dialog.widgets.input import MessageInput


async def save_module(callback: ChatEvent, select: Any, dialog_manager: DialogManager, item_id: str):
	dialog_manager.dialog_data['module'] = item_id
	await dialog_manager.next()


async def save_page_for_exam_preparation_exercises(callback: ChatEvent, select: Any, dialog_manager: DialogManager,
                                                   item_id: str):
	dialog_manager.dialog_data['page_for_exam_preparation_exercises'] = item_id
	await dialog_manager.next()


async def save_paragraph(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
	dialog_manager.dialog_data['paragraph'] = message.text
	await dialog_manager.next()
