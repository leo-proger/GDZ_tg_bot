from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, URLInputFile, ReplyKeyboardRemove

from config import SUBJECTS
from keyboards.choice_gdz import select_subject_kb
from main import bot
from parser import get_solve

router = Router()


class Form(StatesGroup):
	subject = State()
	page = State()


@router.message(Command('start'))
async def greeting_and_choice_subject(message: Message, state: FSMContext):
	await state.set_state(Form.subject)

	await message.answer(f'Привет, {message.from_user.first_name}')

	kb = select_subject_kb()

	await message.answer('Выбери предмет 🗃', reply_markup=kb)


@router.message(Form.subject)
async def choice_page(message: Message, state: FSMContext):
	if message.text in SUBJECTS['with_pages'].values():
		await state.update_data(subject=message.text)
		await state.set_state(Form.page)

		await message.answer('Введи страницу 📃', reply_markup=ReplyKeyboardRemove())
	else:
		await message.reply('Готового Домашнего Задания к такому предмету у меня еще нет 😕')


@router.message(Form.page)
async def choice_exercise(message: Message, state: FSMContext):
	if message.text.isdigit():
		await state.update_data(page=message.text)
		data = await state.get_data()

		# Список url фото с решениями и название файла
		result = get_solve(data=data, pages=True)

		if result['status_code'] != 404:
			title = result['title']

			for url in result['solutions']:
				image = URLInputFile(url, filename=title)
				await bot.send_photo(chat_id=message.chat.id, photo=image)
			await message.answer(title)
		else:
			await message.answer('Страница не найдена')
	else:
		await message.reply('Такой страницы не существует')
