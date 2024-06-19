from sqlalchemy import Column, String

from ..db.postgresdb import Base
from ..utils.departments import find_department
from ..utils.utils import cannonize


class CertifiedMunicipality(Base):
    """
    Represents a Certified Municipality
    """

    __tablename__ = "certified_municipality"

    ugf = Column(String, primary_key=True, index=True)
    town_hall_name = Column(String)
    address = Column(String)
    zip_code = Column(String)
    phone_number = Column(String)
    website = Column(String)
    city_name = Column(String)
    appointment_details = Column(String)
    service_opening_date = Column(String)
    label = Column(String)

    def complete(self):
        department_code, department_name = find_department(self.zip_code)
        cannonized_name = cannonize(self.city_name)

        return {
            "ugf": self.ugf,
            "town_hall_name": self.town_hall_name,
            "address": self.address,
            "zip_code": self.zip_code,
            "phone_number": self.phone_number,
            "website": self.website,
            "city_name": self.city_name,
            "appointment_details": self.appointment_details,
            "service_opening_date": self.service_opening_date,
            "label": self.label,
            "department_code": department_code,
            "department_name": department_name,
            "cannonized_name": cannonized_name,
        }
