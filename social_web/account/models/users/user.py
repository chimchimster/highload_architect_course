import asyncio
import datetime
from typing import Callable

from highload_architect_course.social_web.account.models.utils import UserModel, QueryTemplate, DatabaseHandler




class User(UserModel, QueryTemplate):
    """ Класс-представление для миграции объекта пользователя в СУБД. """


    __available_methods__ = [
        'create_user',
    ]

    def __init__(self, first_name, last_name, password, email, date_of_birth, handler: DatabaseHandler, table='users'):
        super().__init__(first_name, last_name, password, email, date_of_birth)
        self._table = table
        self._handler = handler


    @property
    def table_of_users(self) -> str:
        return self._table

    async def create_user(self) -> str:
        query = self.CREATE_USER_TEMPLATE.format(
            table=self.table_of_users,
            email=self.email,
            first_name=self.first_name,
            last_name=self.last_name,
            password_hash=self.password,
            date_of_birth=self.date_of_birth,
        )
        return query

    async def execute(self, func: Callable):
        for method_name in self.__available_methods__:
            if method_name == func.__name__:
                await self._handler.execute_operation(func)

async def main():
    handler = DatabaseHandler()
    u = User(
        'artem',
        'kasyan',
        'password1',
        'email@email.com',
        datetime.datetime(1994, 5, 6),
        handler,
    )

    await u.execute(u.create_user)


if __name__ == '__main__':
    asyncio.run(main())