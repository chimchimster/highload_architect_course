import asyncio
import datetime

from highload_architect_course.social_web.account.models.utils import UserModel, QueryTemplate, DatabaseHandlerDecorator
from highload_architect_course.social_web.account.models.utils.db_handler import DatabaseHandler


class User(UserModel, QueryTemplate):
    """ Класс-представление для миграции объекта пользователя в СУБД. """


    def __init__(self, first_name, last_name, password, email, date_of_birth, table='users'):
        super().__init__(first_name, last_name, password, email, date_of_birth)
        self._table = table

    @property
    def table_of_users(self) -> str:
        return self._table

    @DatabaseHandlerDecorator()
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



async def main():
    handler = DatabaseHandler()

    u = User(
        'artem',
        'kasyan',
        'password1',
        'email@email.com',
        datetime.datetime(1994, 5, 6),
    )

    await handler.execute(u.create_user)

if __name__ == '__main__':
    asyncio.run(main())
