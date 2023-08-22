import os
import asyncio
from dotenv import load_dotenv
import aiomysql

load_dotenv()

class AccountDatabase:
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    async def pool(self):
        loop = asyncio.get_event_loop()
        return await aiomysql.create_pool(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.database,
            loop=loop,
            autocommit=False,
            minsize=5,
            maxsize=10,
    )

    async def select_all(self):
        pool = await self.pool()
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await cursor.execute("SHOW TABLES")
                result = await cursor.fetchall()
                print(result)

    async def create_user_table(self):
        pool = await self.pool()
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                await connection.begin()
                try:
                    query = """
                        CREATE TABLE IF NOT EXISTS users (
                            id int PRIMARY KEY AUTO INCREMENT,
                            email VARCHAR(100) NOT NULL,
                            first_name VARCHAR(35) NOT NULL,
                            last_name VARCHAR(35) NOT NULL,
                            password_hash VARCHAR(128) NOT NULL,
                            date_of_birth DATETIME NOT NULL,
                            date_joined DATETIME NOT NULL,
                            date_edited DATETIME NOT NULL,
                            blocked Boolean NOT NULL DEFAULT False,
                            is_staff Boolean NOT NULL DEFAULT False,
                            is_super_user Boolean NOT NULL DEFAULT False, 
                        )
                    """
                    await cursor.execute(query)
                    await connection.commit()
                except Exception as e:
                    await connection.rollback()
                    print(e)

    async def create_user(self):
        pass

async def main():
    db = AccountDatabase(
        os.environ.get('MYSQL_HOST'),
        3306,
        os.environ.get('MYSQL_USER'),
        os.environ.get('MYSQL_PASSWORD'),
        'temp_db',
    )
    await db.create_user_table()


if __name__ == '__main__':

    asyncio.run(main())