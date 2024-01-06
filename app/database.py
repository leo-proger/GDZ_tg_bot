import aiomysql

from .config import MYSQL_HOST, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE


class Users:
	@staticmethod
	async def add_user(telegram_id: int, first_name: str = None, last_name: str = None) -> dict[str: int]:
		pool = await aiomysql.create_pool(
			host=MYSQL_HOST,
			user=MYSQL_USER,
			password=MYSQL_PASSWORD,
			db=MYSQL_DATABASE
			)

		async with pool.acquire() as conn:
			async with conn.cursor() as cur:
				# Проверка наличия пользователя в базе данных
				await cur.execute('SELECT * FROM Users WHERE telegram_id = %s', (telegram_id,))
				user = await cur.fetchone()

				# Если пользователь не найден, добавляем его в базу данных
				if user is None:
					await cur.execute('INSERT INTO Users (telegram_id, first_name, last_name) VALUES (%s, %s, %s)',
					                  (telegram_id, first_name, last_name))
					await conn.commit()
					return {'status_code': 200}
				return {'status_code': 409}

	@staticmethod
	async def get_users() -> list:
		pool = await aiomysql.create_pool(
			host=MYSQL_HOST,
			user=MYSQL_USER,
			password=MYSQL_PASSWORD,
			db=MYSQL_DATABASE
			)
		async with pool.acquire() as conn:
			async with conn.cursor() as cur:
				await cur.execute("SELECT telegram_id FROM Users")

				rows = await cur.fetchall()
				users = [row[0] for row in rows]
		return users

