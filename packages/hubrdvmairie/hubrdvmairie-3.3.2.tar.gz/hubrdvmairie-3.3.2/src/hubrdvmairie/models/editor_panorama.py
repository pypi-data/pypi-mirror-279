from sqlalchemy import Boolean, Column, Integer, String

from ..db.postgresdb import Base


class EditorPanorama(Base):
    __tablename__ = "editor_panorama"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    logo_url = Column(String, nullable=True)
    site_url = Column(String, nullable=True)
    contact_url = Column(String, nullable=True)
    overseas = Column(Boolean)
    integration_predemande = Column(Boolean)
    limit_appointment_outside = Column(Boolean)
    saas = Column(Boolean)
    use_queue = Column(Boolean)
    is_connect_to_hub = Column(Boolean)
    is_connect_to_anti_duplication = Column(Boolean)
