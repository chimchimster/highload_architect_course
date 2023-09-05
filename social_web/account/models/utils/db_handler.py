import os

import aiopg
import psycopg2
import asyncio
from dotenv import load_dotenv
from functools import wraps
from typing import Callable, Any


class DatabaseHandler:
    def __init__(self):
        load_dotenv()
        self._db_name = os.environ.get('pg_host')
        self._user = os.environ.get('pg_user')
        self._password = os.environ.get('pg_password')
        self._host = os.environ.get('pg_host')
        self._dsn = f'dbname={self.db_name} user={self.user} password={self.password} host={self.host}'

    @property
    def db_name(self) -> str:
        return self._db_name

    @property
    def user(self) -> str:
        return self._user

    @property
    def password(self) -> str:
        return self._password

    @property
    def host(self) -> str:
        return self._host

    @property
    def dsn(self) -> str:
        return self._dsn

    async def execute_operation(self, func: Callable) -> Any:
        async with aiopg.create_pool(self.dsn, timeout=3.0, minsize=5, maxsize=10) as pool:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    @wraps(func)
                    async def wrapper(*args, **kwargs):
                        try:
                            await cursor.execute('BEGIN')
                            query = await func(*args, **kwargs)

                            await cursor.execute(query)
                            await cursor.execute('COMMIT')
                        except asyncio.TimeoutError as exc:
                            await cursor.execute('ROLLBACK')
                            raise exc
                        except psycopg2.Error as exc:
                            await cursor.execute('ROLLBACK')
                            raise exc

                    return wrapper

