from datetime import datetime
from abc import ABC, abstractmethod


class UserModel(ABC):
    def __init__(
            self,
            first_name: str,
            last_name: str,
            password: str,
            email: str,
            date_of_birth: datetime,
    ):
        self._first_name = first_name
        self._last_name = last_name
        self._password = password
        self._email = email
        self._date_of_birth = date_of_birth

    @property
    def first_name (self) -> str:
        return self._first_name

    @property
    def last_name (self) -> str:
        return self._last_name

    @property
    def password (self) -> str:
        return self._password

    @property
    def email (self) -> str:
        return self._email

    @property
    def date_of_birth (self) -> datetime:
        return self._date_of_birth

    @abstractmethod
    async def create_user(self):
        """ Метод предназначенный для создания объекта пользователя в СУБД. """

