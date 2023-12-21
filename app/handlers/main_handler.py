from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from app import config
from app.keyboards.keyboards import book_selection_kb, EnglishKeyboards
from main import bot

from .english import FormEnglish, english_router

router = Router()
router.include_routers(
	english_router,
	)

english_kb = EnglishKeyboards()


class MainForm(StatesGroup):
	book = State()  # Отдельный учебник какого-то автора


@router.message(Command('list'))
async def book_selection(message: Message, state: FSMContext) -> None:
	await state.set_state(MainForm.book)

	await message.answer('Выбери учебник 📐📓📊📘', reply_markup=book_selection_kb())


@router.message(MainForm.book)
async def numbering_selection(message: Message, state: FSMContext) -> None:
	subject = message.text.split(' ', 1)[0].lower()

	if subject == 'английский':
		await state.update_data(book=message.text)

		# Отправляем сообщение с клавиатурой для удаления
		bot_message = await message.answer('Теперь выбери раздел 📑', reply_markup=ReplyKeyboardRemove())

		# Затем редактируем сообщение с обновленной клавиатурой
		await bot.edit_message_text('Теперь выбери раздел 📑', chat_id=message.chat.id,
		                            message_id=bot_message.message_id,
		                            reply_markup=english_kb.section_selection_kb(message.text))
	else:
		await message.reply('Такого учебника, у меня нет 😕', reply_markup=ReplyKeyboardRemove())
		await state.clear()

# @router.message(FormBook.numbering)
# async def get_solve(message: Message, state: FSMContext) -> None:
# 	if check_numbering(message.text):
# 		await state.update_data(numbering=message.text)
# 		data = await state.get_data()
#
# 		book = data.get('book', '')
# 		numbering = data.get('numbering', '')
#
# 		parser = Parser(book, numbering)
# 		result = await parser.get_solution_data()
#
# 		if result:
# 			solution = result.get('solution')
# 			title = result.get('title')
#
# 			await send_solution(message, solution, title)
# 		else:
# 			await message.answer('Не найдено 😕', reply_markup=ReplyKeyboardRemove())
# 	else:
# 		await message.answer('Не найдено 😕', reply_markup=ReplyKeyboardRemove())
# 	await state.clear()
