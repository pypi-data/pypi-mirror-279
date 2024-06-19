from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship

from ..db.postgresdb import Base
from .meeting_point import MeetingPoint  # noqa: F401
from .token_ants_to_editor import TokenAntsToEditor  # noqa: F401
from .token_editor_to_ants import TokenEditorToAnts  # noqa: F401


class Editor(Base):
    """
    Represents an editor entity in the database.
    """

    __tablename__ = "editor"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    url = Column(String, nullable=False)
    header_name = Column(String, nullable=False)
    only_connect_to_anti_duplication = Column(Boolean)
    tokens_ants_to_editor = relationship("TokenAntsToEditor", back_populates="editor")
    tokens_editor_to_ants = relationship("TokenEditorToAnts", back_populates="editor")
    meeting_points = relationship("MeetingPoint", back_populates="editor")

    def clean_token(self):
        """
        Removes invalid tokens from the lists of tokens.
        """

        self.tokens_ants_to_editor = [
            token for token in self.tokens_ants_to_editor if token.is_valid()
        ]
        self.tokens_editor_to_ants = [
            token for token in self.tokens_editor_to_ants if token.is_valid()
        ]

    def to_dto(self):
        """
        Converts the Editor object to a DTO object.
        Clear token list before conversion: a token is valid if the validity date is in the future or not set.
        Returns:
            DTO: A DTO object representing the Editor.
        """

        from .editor import Editor as DTO  # noqa: F401

        self.clean_token()
        return DTO(
            url=self.url,
            name=self.name,
            test_mode=False,
            header_name=self.header_name,
            tokens_editor_to_ants=self.tokens_editor_to_ants,
            tokens_ants_to_editor=self.tokens_ants_to_editor,
            status=False,
        )
