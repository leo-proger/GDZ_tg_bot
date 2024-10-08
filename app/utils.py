import asyncio
import re

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, URLInputFile

from app import config
from app.parser import get_solve
from main import bot


async def get_solve_data(message: Message, state: FSMContext, data_key: str, error_message: str) -> None:
    if message.text.isdigit() or message.text.replace('.', '', 1).isdigit():
        await state.update_data({data_key: message.text})

        # book, page or exercise or number
        data: dict = await state.get_data()

        # Список url фото с решениями
        result = await get_solve(**data)
        status_code = result.get('status_code', 500)

        if status_code == 200:
            title = result.get('title')
            solution = result.get('solution')

            await send_solve(message=message, solution=solution, title=title)
        elif status_code == 404:
            text, suffix = result.get('text'), result.get('suffix')
            await message.answer(config.ERROR_MESSAGE_404.format(text, suffix))
        elif status_code == 500:
            await message.answer(config.ERROR_MESSAGE_500)
    else:
        await message.reply(error_message)
    await state.clear()


async def send_solve(message: Message, solution: list[str] | str, title: str) -> None:
    if isinstance(solution, str):
        for text in split_text(solution):
            await message.answer(text)
    else:
        for url in solution:
            image = URLInputFile(url, filename=title)
            await bot.send_photo(chat_id=message.chat.id, photo=image)

            # Задержка после отправки, чтобы телеграм не выдавал ошибку
            await asyncio.sleep(config.MESSAGE_DELAY)

        await message.answer(title)


def split_text(text: str, max_length: int = 4096):
    # Находим границы предложений и абзацев
    boundaries = list(re.finditer(r'(?<=[.!?])\s+|\n', text))

    # Добавляем начало и конец текста в границы
    boundaries = [(-1, 0)] + [(m.start(), m.end()) for m in boundaries] + [(len(text), len(text))]

    # Объединяем предложения и абзацы, пока они не достигнут максимальной длины
    parts = []
    start = 0
    for i in range(1, len(boundaries)):
        if boundaries[i][0] - start > max_length:
            parts.append(text[start:boundaries[i - 1][1]])
            start = boundaries[i - 1][1]
    parts.append(text[start:])

    return parts
