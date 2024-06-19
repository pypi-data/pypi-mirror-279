from pydantic import BaseModel


class EditorBase(BaseModel):
    """
    Base editor schema.
    """

    name: str
    url: str
    header_name: str


class EditorCreate(EditorBase):
    """
    Editor create schema.
    """


class EditorUpdate(EditorBase):
    """
    Editor update schema.
    """


class Editor(EditorBase):
    """
    Editor schema.
    """

    id: int

    class Config:
        orm_mode = True
