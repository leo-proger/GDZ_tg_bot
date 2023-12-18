import aiomysql
from .config import MYSQL_ROOT_PASSWORD


class User:
	def __init__(self, telegram_id: int, first_name: str = None, last_name: str = None) -> None:
		self.telegram_id = telegram_id
		self.first_name = first_name
		self.last_name = last_name

	async def add_user(self) -> dict[str: int]:
		pool = await aiomysql.create_pool(
			host='mysql',
			user='root',
			password=MYSQL_ROOT_PASSWORD
			)

		async with pool.acquire() as conn:
			async with conn.cursor() as cur:
				# Проверка наличия пользователя в базе данных
				await cur.execute('SELECT * FROM Users WHERE telegram_id = %s', (self.telegram_id,))
				user = await cur.fetchone()

				# Если пользователь не найден, добавляем его в базу данных
				if user is None:
					await cur.execute('INSERT INTO Users (telegram_id, first_name, last_name) VALUES (%s, %s, %s)',
					                  (self.telegram_id, self.first_name, self.last_name))
					await conn.commit()
					return {'status_code': 200}
				return {'status_code': 409}
