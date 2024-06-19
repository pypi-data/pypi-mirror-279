from pydantic import BaseModel


class MeetingPointBase(BaseModel):
    """
    MeetingPoint editor schema.
    """

    ugf: str
    editor_name_and_id: str
    id_editor: int
    city_name: str


class MeetingPointCreate(MeetingPointBase):
    """
    MeetingPoint create schema.
    """


class MeetingPointUpdate(MeetingPointBase):
    """
    MeetingPoint update schema.
    """


class MeetingPoint(MeetingPointBase):
    """
    MeetingPoint schema.
    """

    class Config:
        orm_mode = True
