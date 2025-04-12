from app.database import Base
from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Table(Base):
    __tablename__ = 'table'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    seats: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    location: Mapped[str] = mapped_column(String(100), nullable=False, index=True)

    @property
    def dict_(self):
        return {
            "id": self.id,
            "name": self.name,
            "seats": self.seats,
            "location": self.location
        }
