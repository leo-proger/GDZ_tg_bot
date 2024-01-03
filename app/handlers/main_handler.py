from aiogram import Router
from aiogram.filters import Command

from ..dialogs import *
from ..dialogs import main_dialog
from ..states import MainForm

router = Router()
router.include_routers(
	main_dialog,
	dialog_english,
	dialog_russian,
	dialog_math,
	dialog_geometry,
	dialog_sociology,
	dialog_physics
	)


@router.message(Command('list'))
async def book_selection(message: Message, dialog_manager: DialogManager) -> None:
	await dialog_manager.start(MainForm.book)
