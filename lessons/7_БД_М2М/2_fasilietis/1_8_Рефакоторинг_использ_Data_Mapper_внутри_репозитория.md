Задача: Дописать остальные мапперы и реализовать подсказку типов

```python
from typing import TypeVar  # импртируем класс TypeVar

from pydantic import BaseModel  # импорт BaseModel
from src.database import Base  # импорт Base

# переменная SchemaType ссылается на класс привязывая имя переменной к типу BaseModel
SchemaType = TypeVar("SchemaType", bound=BaseModel)
# переменная ссылается на тип Base, которая хранит всю информацию о модели 
DBModelType = TypeVar("DBModelType", bound=Base)


class DataMapper:
    db_model: type[DBModelType] = None  # модель алхимии HotelsOrm
    schema: type[SchemaType] = None  # пайдентик схема Hotel

    @classmethod
    def map_to_domain_entity(cls, data):
        """
        Метод принимает в качестве аргумента данные алхимии и
        возвращает пайдантик схему
        """
        return cls.schema.model_validate(data, from_attributes=True)

    @classmethod
    def map_to_persistence_entity(cls, data):
        """
        метод принимает данные пайдантик схемы и возвращает объект модели алхимии
        """
        return cls.db_model(**data.model_dump)


``` 

Реализуем все мапперы для осталных классов

```python


class HotelMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel


class RoomsMapper(DataMapper):
    db_model = RoomsOrm
    schema = Room


class FacilitiesMapper(DataMapper):
    db_model = FacilitiesOrm
    schema = Facility


class BookingMapper(DataMapper):
    db_model = BookingsOrm
    schema = Booking


class UserDataMapper(DataMapper):
    db_model = UsersOrm
    schema = User


class RoomDataWithRelsMapper(DataMapper):
    db_model = RoomsOrm
    schema = RoomWitchRels
```

Для каждого класса репозитория убираем атрибут относящийся к схеме и дописываем
атрибут mapper = HotelsMapper для репозитория отелей
