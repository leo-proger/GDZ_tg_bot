import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from app.config import TOKEN
from app.handlers import main_handler, default_handlers
from app.middlewares.add_user_to_db_middleware import AddUserToDatabaseMiddleware
from app.users.database import create_users_table

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='Markdown'))


async def main():
    await create_users_table()

    dp = Dispatcher()

    main_handler.router.message.middleware(AddUserToDatabaseMiddleware())
    default_handlers.router.message.middleware(AddUserToDatabaseMiddleware())

    dp.include_routers(
        main_handler.router,
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
