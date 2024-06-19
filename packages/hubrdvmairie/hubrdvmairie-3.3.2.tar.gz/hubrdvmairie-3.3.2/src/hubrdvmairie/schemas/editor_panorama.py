from pydantic import BaseModel


class EditorPanoramaBase(BaseModel):
    """
    Base editor schema.
    """

    name: str
    logo_url: str
    site_url: str
    contact_url: str
    overseas: bool
    integration_predemande: bool
    limit_appointment_outside: bool
    saas: bool
    use_queue: bool
    is_connect_to_hub: bool
    is_connect_to_anti_duplication: bool


class EditorPanoramaCreate(EditorPanoramaBase):
    """
    Editor create schema.
    """


class EditorPanoramaUpdate(EditorPanoramaBase):
    """
    Editor update schema.
    """


class EditorPanorama(EditorPanoramaBase):
    """
    Editor schema.
    """

    id: int

    class Config:
        orm_mode = True
