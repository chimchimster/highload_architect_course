from ..utils import UserModel, QueryTemplate, DatabaseHandler


class User(UserModel, QueryTemplate):
    """ Класс-представление для миграции объекта пользователя в СУБД.
        Используется паттерн-проектирования "Dependency Injection", т.е.
        данный класс будет иметь зависимость в виде аргумента (экземпляра класса DatabaseHandler). """


    def __init__(self, first_name, last_name, password, email, date_of_birth, connection: DatabaseHandler, table='Users'):
        super().__init__(first_name, last_name, password, email, date_of_birth)
        self._connection = connection
        self._table = table

    @property
    def connection(self) -> DatabaseHandler:
        return self._connection

    @property
    def table_of_users(self) -> str:
        return self._table

    @connection.execute_operation
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
