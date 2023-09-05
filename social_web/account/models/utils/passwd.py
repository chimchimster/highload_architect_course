import bcrypt


async def hash_password(password: str) -> str:
    """ Фукнция для генерации хэша пароля. """

    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password.decode('utf-8')


async def check_password(input_password: str, hashed_password: str) -> bool:
    """ Функция проверки пароля на соответствие хэшу. """

    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password.encode('utf-8'))

