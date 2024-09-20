from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String

class HotelsOrm(Base):
    __tablename__ = "hotels"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    location: Mapped[str]

    def __repr__(self):
        return f"Отель: {self.title}, {self.location}"