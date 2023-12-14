import aiosqlite

from .config import DATABASE_PATH


class User:
	def __init__(self, telegram_id: int, first_name: str = None, last_name: str = None) -> None:
		self.telegram_id = telegram_id
		self.first_name = first_name
		self.last_name = last_name

	async def add_user(self) -> dict[str: int]:
		async with aiosqlite.connect(DATABASE_PATH) as db:
			async with db.cursor() as cur:
				# Проверка наличия пользователя в базе данных
				await cur.execute('SELECT * FROM Users WHERE telegram_id = ?', (self.telegram_id,))
				user = await cur.fetchone()

				# Если пользователь не найден, добавляем его в базу данных
				if user is None:
					await cur.execute('INSERT INTO Users ("telegram_id", "first_name", "last_name") VALUES (?, ?, ?)',
					                  (self.telegram_id, self.first_name, self.last_name))
					await db.commit()
					return {'status_code': 200}
				return {'status_code': 409}
