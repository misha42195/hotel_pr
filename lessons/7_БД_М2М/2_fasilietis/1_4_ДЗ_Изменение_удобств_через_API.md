Задание №16: Изменение удобств номера через API
Необходимо вместе с редактированием номеров через PUT и PATCH дать
возможность редактировать удобства номера.
То есть новых ручек создавать не нужно — все задание решается
внутри уже существующих ручек на изменение номера.

Звучит просто. Но на деле всё сложнее.
У номера уже могут быть какие-то удобства, например,
с айдишниками 1 и 2. А пользователь решил убрать удобство 1 и добавить удобство 3.
Теперь, нам как бэкендерам, необходимо удалить из m2m таблицы
удобство 1 и добавить удобство 3. В идеале оставить удобство 2 нетронутым, чтобы
Запросы происходили быстрее (т.к. часть данных не изменяется)
Столбец id не рос слишком быстро. А то может случиться так,
что он превысит лимит и нам придется тратить память, чтобы увеличить лимит
столбца id (речь про тип bigint в PostgreSQL)

Задача в том, чтобы придумать рабочий способ определения тех удобств,
которые нуждаются в удалении или добавлении. И
произвести манипуляции вставки или удаления только с ними.
А нетронутые удобства оставить нетронутыми

1) Все изменения будут происходить в ручке изменения номера, но само изменения номера не
   будет, изменения коснуться только таблицы room_facility

```python

@router.put("/{hotel_id}/rooms", summary="Полное изменение номера")
async def full_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomRequestAdd,
        db: DBDep
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edite(data=_room_data, id=room_id)
    await db.rooms_facilities.set_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "ok", }
```

await db.rooms_facilities.set_facilities(room_id=room_id,facilities_ids=room_data.facilities_ids)
в данной строке кода вызываем метод set_facilities в качестве аргументов передаем room_id и список idшников

в репозитории RoomFacilitiesRepository создадим метод для изменения таблицы room_facility

```python

class RoomsFacilitiesRepository(BaseRepository):
    model = RoomsFacilitiesORM
    schema = RoomFacility

    async def set_facilities(self, room_id: int, facilities_ids: list[int]) -> None:
        # напишем запрос на получение всех facility_id из таблицы room_facility
        # переменная ссылается на запрос с помощью которого получим список удобств
        get_current_facilities_query = (
            select(self.model.facility_id)
            .filter_by(room_id=room_id)
        )
        # отправим запрос в базу данных получим итератор
        res = await self.session.execute(get_current_facilities_query)
        # переменная ссылается на список значений удобств
        current_facilities_ids: list[int] = res.scalars().all()

        # находим элементы для удаления для 
        # удаляем значения из базы которых нет у клиента 
        # получим список удобств которые необходимо удалить(удаляем значения, которые в списке)
        ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))

        # добавляем все значения которые есть у клиента, но нет в базе 
        ids_to_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

        if ids_to_delete:  # если список не пуст
            delete_stmt = (  # напишем запрос на удаление в котором укажем что у объектов в таблице должны совпасть 
                delete(self.model)  # поля room_id и id удобств должны быть в списке для удаления
                .filter(
                    self.model.room_id == room_id,
                    self.model.facility_id.in_(ids_to_delete))
            )
            await self.session.execute(delete_stmt)  # отправляем запрос в базу 

        if ids_to_insert:  # если список для добавления не пуст
            insert_stmt = (  # напишем запрос на добавление значений 
                insert(self.model)  # сформируем словарь для добавления значений, где room_id возьмем из входящего 
                # аргумента, id удобств из списка для добавления
                .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert])
            )
            await self.session.execute(insert_stmt)  # исполним запрос 
```

В схеме на изменение номера добавим параметр в который передадим список удобств для изменения

```python
class RoomRequestAdd(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = [] # список id удобств
```
лучение удобств номера через relationship

Напомним что наши таблицы такие как rooms и facilities связаны между собой
таблицей многие ко многим rooms_facilities
Но мы так же можем получать значения из связанных таблиц установив связь relationship
связь relationship устанавливается только для таблиц у которых определены внешние ключи

```python
class RoomsOrm(Base):  # наследуемся от базового класса 
    __tablename__ = "rooms"  # имя таблицы 
    __table_args__ = {'extend_existing': True}  # 

    id: Mapped[int] = mapped_column(primary_key=True)  # первичный ключ
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[int] = mapped_column(String)
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]

    # атрибут ссылается на список объектов удобств через обратную связь 
    facilities: Mapped[list["FacilitiesOrm"]] = relationship(
        back_populates="rooms",
        secondary="rooms_facilities",

    )

```

Такую же связь необходимо установить в таблице Facility

```python

class FacilitiesOrm(Base):
    __tablename__ = "facilities"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))

    # атрибут через который связываем удобства с таблицей номеров 
    rooms: Mapped[list["RoomsOrm"]] = relationship(
        back_populates="facilities",
        secondary="rooms_facilities",
    )

```

```python
@router.put("/{hotel_id}/rooms", summary="Полное изменение номера")
async def full_edit_room(
        hotel_id: int,  # обязательный параметр id отеля
        room_id: int,  # обязательный параметр id номера 
        room_data: RoomRequestAdd,  # схема объекта запроса входящих данных для добавления номера
        db: DBDep  # объект зависимость-контекстный менеджер
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())  # схема со значениями для добавления номера  
    await db.rooms.edite(data=_room_data, id=room_id)  # вызываем метод с отправкой запроса в базу данных 
    # вызываем метод для установки удобств для конкретного номера, передаем id номера и передадим значения id удобств
    await db.rooms_facilities.set_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "ok", }
```

Для того что бы при получении номеров получить и его удобства необходимо установить в схеме номеров
атрибут facilities

```python
class RoomRequestAdd(BaseModel):
    title: str
    description: str | None = None
    price: int
    quantity: int
    facilities_ids: list[int] = []  # список хранит id-и с удобствами номеров
```

```python
@router.put("/{hotel_id}/rooms", summary="Полное изменение номера")
async def full_edit_room(
        hotel_id: int,
        room_id: int,
        room_data: RoomRequestAdd,
        db: DBDep
):
    _room_data = RoomAdd(hotel_id=hotel_id, **room_data.model_dump())
    await db.rooms.edite(data=_room_data, id=room_id)
    await db.rooms_facilities.set_facilities(room_id=room_id, facilities_ids=room_data.facilities_ids)
    await db.commit()
    return {"status": "ok"}

```

для установки удобств для конкретного номера должны передать id номера, список id удобств

```python
async def set_facilities(self, room_id: int, facilities_ids: list[int]) -> None:
    # напишем запрос на получение всех facility_id из таблицы room_facility
    get_current_facilities_query = (  # получаем текущие id удлбства у текущего номера по room_id
        select(self.model.facility_id)  # 
        .filter_by(room_id=room_id)
    )
    # отправим запрос в базу данных
    res = await self.session.execute(get_current_facilities_query)
    current_facilities_ids: list[int] = res.scalars().all()  # ссылка на текущие удобства

    # находим элементы для удаления для этого
    # находим разность между списками от клиента и из базы
    ids_to_delete: list[int] = list(set(current_facilities_ids) - set(facilities_ids))

    # добавляем все значения которые есть у клиента, но нет в базе 
    ids_to_insert: list[int] = list(set(facilities_ids) - set(current_facilities_ids))

    if ids_to_delete:
        delete_stmt = (
            delete(self.model)
            .filter(
                self.model.room_id == room_id,
                self.model.facility_id.in_(ids_to_delete))
        )
        await self.session.execute(delete_stmt)  # отправляем запрос на удаления значений удобств

    if ids_to_insert:
        insert_stmt = (
            insert(self.model)
            .values([{"room_id": room_id, "facility_id": f_id} for f_id in ids_to_insert])
        )  # отправляем запрос на добавление значений в базу данных 
        await self.session.execute(insert_stmt)  # 
```
