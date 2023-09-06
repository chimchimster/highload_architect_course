import os

import aiopg
import psycopg2
import asyncio
from dotenv import load_dotenv
from functools import wraps
from typing import Callable, Any


class DatabaseHandler:

    __available_methods__ = [
        'create_user',
        'wrapper',
    ]


    def __init__(self):
        load_dotenv()
        self._db_name = os.environ.get('pg_db_name')
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

    async def __handle_operation(self, func: Callable) -> Any:
        """ Метод-обертка позволяющий выполнять операции в PostgreSQL. """

        async with aiopg.create_pool(self.dsn, timeout=3.0, minsize=5, maxsize=10) as pool:
            async with pool.acquire() as connection:
                async with connection.cursor() as cursor:
                    @wraps(func)
                    async def wrapper(*args, **kwargs):
                        try:
                            query = await func(*args, **kwargs)
                            await cursor.execute(query)
                        except asyncio.TimeoutError as exc:
                            raise exc
                        except psycopg2.Error as exc:
                            raise exc

                    return wrapper

    async def execute (self, func: Callable, *args, **kwargs) -> Any:
        for method_name in self.__available_methods__:
            if method_name == func.__name__:
                wrapped_result = await self.__handle_operation(func)
                return await wrapped_result(*args, **kwargs)

        raise ValueError(f'Метод {func.__name__} не доступен в данном классе!')


class DatabaseHandlerDecorator:
    def __init__(self):
        self.handler = DatabaseHandler()

    def __call__(self, func):
        async def wrapper(instance, *args, **kwargs):
            await self.handler.execute(func, instance, *args, **kwargs)
        return wrapper