import asyncio
import logging

from aiogram import Bot, Dispatcher

import config
from handlers import subject_selection_handlers, default_handlers

logging.basicConfig(level=logging.INFO)

bot = Bot(token=config.TOKEN, parse_mode='Markdown')


async def main():
	dp = Dispatcher()

	dp.include_routers(
		subject_selection_handlers.router,
		default_handlers.router,
		)

	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)


if __name__ == '__main__':
	print('Бот работает...')
	try:
		asyncio.run(main())
	except KeyboardInterrupt:
		print('Бот закончил работу.')
