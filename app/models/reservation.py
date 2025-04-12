import datetime
from app.database import Base
from sqlalchemy import Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column


class Reservation(Base):
    __tablename__ = 'reservation'

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    table_id: Mapped[int] = mapped_column(ForeignKey('table.id'), nullable=False)
    reservation_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    duration_minutes: Mapped[int] = mapped_column(Integer, nullable=False)
    end_time: Mapped[datetime.datetime] = mapped_column(DateTime(timezone=False), nullable=False)

    @property
    def dict_(self):
        return {
            "id": self.id,
            "customer_name": self.customer_name,
            "table_id": self.table_id,
            "reservation_time": self.reservation_time,
            "duration_minutes": self.duration_minutes,
            'end_time': self.end_time
        }

    def __repr__(self):
        return f'Бронь {self.customer_name} на {self.reservation_time}'
