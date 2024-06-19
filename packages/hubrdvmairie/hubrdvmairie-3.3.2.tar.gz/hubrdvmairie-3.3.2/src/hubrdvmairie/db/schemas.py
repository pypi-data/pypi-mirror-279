"""
This module contains Pydantic schemas for database models related to token and editor entities.
It includes the following schemas:
- TokenAntsToEditorBase
- TokenAntsToEditorCreate
- TokenAntsToEditor
- TokenEditorToAntsBase
- TokenEditorToAntsCreate
- TokenEditorToAnts
- EditorBase
- EditorCreate
- EditorUpdate
- Editor
"""
import datetime

from pydantic import BaseModel


class TokenAntsToEditorBase(BaseModel):
    """
    Base schema for token issued by ANTS to editor
    """

    id: int
    id_editor: int
    token: str
    validity_date: datetime

    class Config:
        orm_mode = True


class TokenAntsToEditorCreate(TokenAntsToEditorBase):
    """
    Schema for creating token issued by ANTS to editor
    """


class TokenAntsToEditor(TokenAntsToEditorBase):
    """
    Schema for token issued by ANTS to editor
    """


class TokenEditorToAntsBase(BaseModel):
    """
    Base schema for token issued by editor to ANTS
    """

    id: int
    id_editor: int
    token: str
    validity_date: datetime

    class Config:
        orm_mode = True


class TokenEditorToAntsCreate(TokenEditorToAntsBase):
    """
    Schema for creating token issued by editor to ANTS
    """


class TokenEditorToAnts(TokenEditorToAntsBase):
    """
    Schema for token issued by editor to ANTS
    """


class EditorBase(BaseModel):
    """
    Base schema for editor
    """

    name: str
    url: str
    header_name: str


class EditorCreate(EditorBase):
    """
    Schema for creating editor
    """


class EditorUpdate(EditorBase):
    """
    Schema for updating editor
    """


class Editor(EditorBase):
    """
    Schema for editor
    """

    id: int

    class Config:
        orm_mode = True


class EditorPanoramaBase(BaseModel):
    """
    Base schema for editor_panorama
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
    Schema for creating editor
    """


class EditorPanoramaUpdate(EditorPanoramaBase):
    """
    Schema for updating editor
    """


class EditorPanorama(EditorPanoramaBase):
    """
    Schema for editor
    """

    id: int

    class Config:
        orm_mode = True
