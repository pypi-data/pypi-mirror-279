from typing import List

from sqlalchemy.orm import Session

from ..crud.base import CRUDBase
from ..models.certified_municipality import CertifiedMunicipality
from ..schemas.certified_municipality import (
    CertifiedMunicipalityCreate,
    CertifiedMunicipalityUpdate,
)


class CRUDCertifiedMunicipality(
    CRUDBase[
        CertifiedMunicipality, CertifiedMunicipalityCreate, CertifiedMunicipalityUpdate
    ]
):
    """
    CRUD operations for the CertifiedMunicipality model.
    """

    def get_all(self, db: Session) -> List[CertifiedMunicipality]:
        """
        Retrieve all CertifiedMunicipality.

        Args:
            db (Session): The database session.

        Returns:
            List[CertifiedMunicipality]: A list of all CertifiedMunicipality.
        """
        return db.query(CertifiedMunicipality).all()

    def update(
        self,
        db: Session,
        *,
        db_obj: CertifiedMunicipality,
        obj_in: CertifiedMunicipality
    ) -> CertifiedMunicipality:
        """
        Update a CertifiedMunicipality.
        """
        db_obj.ugf = obj_in.ugf
        db_obj.town_hall_name = obj_in.town_hall_name
        db_obj.address = obj_in.address
        db_obj.zip_code = obj_in.zip_code
        db_obj.phone_number = obj_in.phone_number
        db_obj.website = obj_in.website
        db_obj.appointment_details = obj_in.appointment_details
        db_obj.service_opening_date = obj_in.service_opening_date
        db.commit()
        return db_obj

    def save_or_update(
        self, db: Session, *, obj_in: CertifiedMunicipality
    ) -> tuple[str, CertifiedMunicipality]:
        """
        Save or update a CertifiedMunicipality.
        """
        certified_municipality = (
            db.query(CertifiedMunicipality)
            .filter(CertifiedMunicipality.ugf == obj_in.ugf)
            .first()
        )
        if certified_municipality:
            self.update(db, db_obj=certified_municipality, obj_in=obj_in)
            return "updated", certified_municipality.ugf
        else:
            self.create(db, obj_in=obj_in)
        return "created", obj_in.ugf


certified_municipality = CRUDCertifiedMunicipality(CertifiedMunicipality)
