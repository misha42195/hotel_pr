Получение удобств номера через relationship

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
Необходимо изменить получение номеров в методе get_filter_by_time()

```python
    async def get_filtered_by_time(
        self,  # ссылка на экземпляр
        hotel_id, # id отеля
        date_from: date, # дата заселения 
        date_to: date): # дата выселения 
    # получаем id свободных номеров доступных для бронирования
    rooms_ids_to_get = rooms_ids_for_booking(date_from, date_to, hotel_id)
    # print(rooms_ids_to_get.compile(engine, compile_kwargs={"literal_binds": True}))
    # return await self.get_filtered(RoomsOrm.id.in_(rooms_ids_to_get))
    query = (# запрос на получение объектов номеров, и данных которые связаны с полем relations, то есть удобств
        # но только тех, для которых id номеров совпадает со списком в rooms_ids_to_get
        select(self.model)
        .options(selectinload(self.model.facilities))
        .filter(RoomsOrm.id.in_(rooms_ids_to_get))
    )
    # получаем результат и получаем значение в переменную result, который возвращается в виде итератора
    # прогоняем  через валидатор схемы в RoomWitchRels проверяет поле id и поле facility, который содержит 
    #  список объектов удобств
    result = await self.session.execute(query)
    return [RoomWitchRels.model_validate(model) for model in result.unique().scalars().all()]

```
