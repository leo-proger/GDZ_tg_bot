from typing import Any

from aiogram_dialog import ChatEvent, DialogManager


async def save_module(callback: ChatEvent, select: Any, dialog_manager: DialogManager, item_id: str):
	dialog_manager.dialog_data['module'] = item_id
	await dialog_manager.next()
