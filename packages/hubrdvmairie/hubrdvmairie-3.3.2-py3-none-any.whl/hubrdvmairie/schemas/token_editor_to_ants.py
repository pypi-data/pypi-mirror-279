import datetime

from pydantic import BaseModel


class TokenEditorToAntsBase(BaseModel):
    """
    Base class for token editor to ants schema.
    """

    id_editor: int
    token: str
    validity_date: datetime.datetime


class TokenEditorToAntsCreate(TokenEditorToAntsBase):
    """
    Class for creating token editor to ants schema.
    """


class TokenEditorToAntsUpdate(TokenEditorToAntsBase):
    """
    Class for updating token editor to ants schema.
    """


class TokenEditorToAnts(TokenEditorToAntsBase):
    """
    Class for token editor to ants schema.
    """

    id: int

    class Config:
        orm_mode = True
