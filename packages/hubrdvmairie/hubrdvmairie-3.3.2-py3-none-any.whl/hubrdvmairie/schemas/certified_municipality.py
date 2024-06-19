from pydantic import BaseModel


class CertifiedMunicipalityBase(BaseModel):
    """
    Certified Municipality  schema.
    """

    ugf: str
    town_hall_name: str
    address: str
    zip_code: str
    city_name: str
    phone_number: str
    website: str
    appointment_details: str
    service_opening_date: str
    label: str


class CertifiedMunicipalityCreate(CertifiedMunicipalityBase):
    """
    Certified Municipality create schema.
    """


class CertifiedMunicipalityUpdate(CertifiedMunicipalityBase):
    """
    Certified Municipality update schema.
    """


class CertifiedMunicipality(CertifiedMunicipalityBase):
    """
    Certified Municipality schema.
    """

    class Config:
        orm_mode = True
