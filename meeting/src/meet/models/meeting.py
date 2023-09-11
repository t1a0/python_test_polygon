from uuid import uuid4
import sys
sys.path.append(sys.path[0] + '/../../..')

from sqlalchemy import Column, String, UUID, DateTime
from sqlalchemy.sql import func

from src.models import Base


class Meeting(Base):
	__tablename__ = 'meeting'

	id = Column(UUID, primary_key=True ,default=uuid4())
	place = Column(String, nullable=False)
	datetime = Column(DateTime, default=func.current_timestamp())

	def __repr__(self) -> str:
		return f"Meeting(id={self.id!r}, place={self.place!r}, datetime={self.datetime!r})"