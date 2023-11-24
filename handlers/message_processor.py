from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, URLInputFile, ReplyKeyboardRemove

from config import SUBJECTS
from keyboards.school_choice import select_subject_kb, select_textbook_series_kb
from main import bot
from parser import get_solve

router = Router()


class Form(StatesGroup):
	subject = State()  # Английский, Русский, Математика и тд
	textbook_series = State()  # Отдельный учебник какого-то автора, серия
	page = State()  # Страница учебника


@router.message(Command('start'))
async def greeting_and_select_subject(message: Message, state: FSMContext) -> None:
	await state.set_state(Form.subject)

	await message.answer(f'Привет, {message.from_user.first_name}')

	kb = select_subject_kb()

	await message.answer('Сначала выбери школьный предмет 📐📏📈📉📊📘', reply_markup=kb)


@router.message(Form.subject)
async def select_textbook_series(message: Message, state: FSMContext) -> None:
	if message.text in SUBJECTS['with_pages']:
		await state.update_data(subject=message.text)
		await state.set_state(Form.textbook_series)

		kb = select_textbook_series_kb(message.text)

		await message.answer('Теперь выбери учебник 📓📘📗', reply_markup=kb)
	else:
		await message.reply('Готового Домашнего Задания к такому предмету у меня еще нет 😕')


@router.message(Form.textbook_series)
async def select_page(message: Message, state: FSMContext) -> None:
	data = await state.get_data()

	# ic(SUBJECTS['with_pages'][subject])
	# ic(data)
	# ic(message.text)
	# ic(message.text in SUBJECTS['with_pages'][subject])

	if message.text in SUBJECTS['with_pages'][data['subject']]:
		await state.update_data(textbook_series=message.text)
		await state.set_state(Form.page)

		await message.answer('И последнее... введи страницу 📃', reply_markup=ReplyKeyboardRemove())
	else:
		await message.reply('Такого учебника, к сожалению, у меня нет 😕')


@router.message(Form.page)
async def select_exercise(message: Message, state: FSMContext) -> None:
	if message.text.isdigit():
		await state.update_data(page=message.text)
		data = await state.get_data()

		# Список url фото с решениями и название файла
		result = get_solve(*data.values(), pages=True)
		status_code = result.get('status_code')

		if status_code == 200:
			title = result['title']

			for url in result['solutions']:
				image = URLInputFile(url, filename=title)
				await bot.send_photo(chat_id=message.chat.id, photo=image)
			await message.answer(title)
		elif status_code == 500:
			await message.answer(
				'Ой, у меня ошибка. Прошу написать ему >>> [Leo Proger](https://t.me/Leo_Proger)',
				parse_mode='MARKDOWN')
		elif status_code == 404:
			await message.answer('Страница не найдена')
	else:
		await message.reply('Такой страницы не существует')
