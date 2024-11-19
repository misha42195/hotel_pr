
1) Внутри директории создадим папку с mappers, в которой создадим файл base.py 
это будет наш базовый маппер, от которого будут наследоваться мапперы (например HotelMapper)
для приведения к объектов SQLAlchemy к объектам схемы и наоборот приведения объектов схемы к модели алхимии,
но в нашем проекте мы не используем данный тип преобразования


```python
class DataMapper:
    db_model = None # модель алхимии HotelsOrm
    schema = None # пайдентик схема Hotel

    def map_to_domain_entity(self,data):
        """
        Метод принимает в качестве аргумента данные алхимии и
        возвращает пайдантик схему
        """
        return self.schema.model_validate(data,from_attributes=True)



    def map_to_persistence_entity(self,data):
        """
        метод принимает данные пайдантик схемы и возвращает объект модели алхимии
        """
        return self.db_model(**data.model_dump)
```
Класс DataMapper представляет собой класс, который реализует два метода для конвертирования 
или преобразования данных из объектов модели алхимии в пайдантик схему и наоборот

метод map_to_domain принимает данные в виде объекта алхимии и преобразует в объект схемы
например отеля, перед возвращением пользователю пройдя валидацию например 
Hotel.model_validate(data)
Вместо self.schema.model_validate(self,data)
пишем  self.mapper.map_to_domain_entity(self,data)

Второй метод может использоваться для добавления объекта в БД
метод принимает объект схемы, который мы как бы разбиваем на словари используя метод
model_dump -> self.HotelOrm.(**data.model_dump)
но мы в нашей программе его не используем

Для использования класса маппера необходимо реализовать конкретные классы-мапперы
1) Создадим файл mappers в директории mappers
в ней создадим класс HotelMapper наследуемся от DataMapper

```python
class HotelMapper(DataMapper):
    db_model = HotelsOrm
    schema = Hotel
```
Далее нам необходимо в базовом классе репозитория добавить атрибут 
mapper:DataMapper = None, а в подклассах репозиторя таких, как HotelsRepository
добавить конкретный атрибут-маппер 
mapper = HotelMapper
