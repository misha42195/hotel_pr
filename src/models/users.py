from src.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import String

class UsersOrm(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(50),unique=True) # значение поля уникально
    first_name: Mapped[str] = mapped_column(String(100))
    last_name: Mapped[str] = mapped_column(String(100))
    hashed_password: Mapped[str] = mapped_column(String)