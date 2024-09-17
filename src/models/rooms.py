from sqlalchemy.orm import Mapped, mapped_column
from src.database import Base
from sqlalchemy import String
from sqlalchemy import ForeignKey


class RoomsOrm(Base):
    __tablename__ = "rooms"
    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    title: Mapped[int] = mapped_column(String)
    description: Mapped[str | None]
    price: Mapped[int]
    quantity: Mapped[int]
