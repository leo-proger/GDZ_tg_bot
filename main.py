import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramForbiddenError
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from app.config import TOKEN
from app.database import Users
from app.handlers import main_handler
from app.middlewares.add_user_to_db_middleware import AddUserToDatabaseMiddleware


async def send_whats_new():
	users = await Users.get_users()

	message = '''
	Привет! Я обновился до версии ***2.0.0***
	
	***Что нового:***
	• Добавлены разделы для учебников
	• Добавлен новый учебник - физика
	• Теперь каждое обновление я буду оповещать вас о нем (если вам это не нравится, то прошу написать владельцу)
	• Исправлены ошибки
	'''
	for user in users:
		try:
			await bot.send_message(user, message)
		# await asyncio.sleep(100)
		except TelegramForbiddenError:
			print('Бот заблокирован пользователем')


logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, parse_mode='Markdown')


async def main():
	dp = Dispatcher(storage=MemoryStorage())
	main_handler.router.message.middleware(AddUserToDatabaseMiddleware())

	dp.include_routers(
		main_handler.router,
		)
	setup_dialogs(dp)
	await bot.delete_webhook(drop_pending_updates=True)

	await asyncio.create_task(send_whats_new())

	await dp.start_polling(bot)


if __name__ == '__main__':
	print('Бот работает...')
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Бот закончил работу.')
