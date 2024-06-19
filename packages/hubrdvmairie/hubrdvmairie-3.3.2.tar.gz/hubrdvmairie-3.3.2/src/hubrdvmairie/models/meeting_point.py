from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db.postgresdb import Base

if TYPE_CHECKING:
    from .editor_model import Editor  # noqa: F401


class MeetingPoint(Base):
    """
    Represents a Meeting point
    """

    __tablename__ = "meeting_point"

    ugf = Column(String, primary_key=True, index=True)
    id_editor = Column(Integer, ForeignKey("editor.id"))
    editor_name_and_id = Column(String, primary_key=True, index=True, unique=True)
    city_name = Column(String, nullable=True)
    editor = relationship("Editor", back_populates="meeting_points")
