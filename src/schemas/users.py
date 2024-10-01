from pydantic import BaseModel, EmailStr, ConfigDict


# схема для входящих параметров пользователя
class UserRequestAdd(BaseModel):
    nickname: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str # параметр входящего пароля конвертируется хеш-функцией

# схема, экземпляр которого используется для сохранения в БД
class UserAdd(BaseModel):
    nickname: str
    email: EmailStr
    first_name: str
    last_name: str
    hashed_password: str  # хешированное значение пароля

# схема для конвертации объекта user в пайдентик-схему, используется паттерн DataMapper,
# ограничение бизнес-логики от логики данных
class User(BaseModel):
    id: int
    nickname: str
    email: EmailStr
    first_name: str
    last_name: str

    model_config = ConfigDict(from_attributes=True)

class UserWithHashedPassword(User):
    hashed_password: str
