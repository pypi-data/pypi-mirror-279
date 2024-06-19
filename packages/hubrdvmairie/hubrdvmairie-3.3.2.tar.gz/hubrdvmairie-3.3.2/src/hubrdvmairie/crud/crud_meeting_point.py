from typing import List

from sqlalchemy.orm import Session

from ..crud.base import CRUDBase
from ..models.meeting_point import MeetingPoint
from ..schemas.meeting_point import MeetingPointCreate, MeetingPointUpdate


class CRUDMeetingPoint(CRUDBase[MeetingPoint, MeetingPointCreate, MeetingPointUpdate]):
    """
    CRUD operations for the MeetingPoint model.
    """

    def get_by_ugf(self, db: Session, *, ugf: str) -> List[MeetingPoint]:
        """
        Retrieve an meeting point by ugf.

        Args:
            db (Session): The database session.
            name (str): The ugf of the meeting point to retrieve.

        Returns:
            Optional[Editor]: The editor with the given name, or None if not found.
        """
        return db.query(MeetingPoint).filter(MeetingPoint.ugf == ugf).all()

    def get_all(self, db: Session) -> List[MeetingPoint]:
        """
        Retrieve all MeetingPoint.

        Args:
            db (Session): The database session.

        Returns:
            List[MeetingPoint]: A list of all MeetingPoint.
        """
        return db.query(MeetingPoint).all()

    def update(
        self, db: Session, *, db_obj: MeetingPoint, obj_in: MeetingPoint
    ) -> MeetingPoint:
        """
        Update a MeetingPoint.
        """
        db_obj.ugf = obj_in.ugf
        db_obj.editor_name_and_id = obj_in.editor_name_and_id
        db_obj.city_name = obj_in.city_name
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def save_or_update(
        self, db: Session, *, obj_in: MeetingPoint
    ) -> tuple[str, MeetingPoint]:
        """
        Save or update a MeetingPoint.
        """
        meeting_point = (
            db.query(MeetingPoint)
            .filter(
                MeetingPoint.ugf == obj_in.ugf,
                MeetingPoint.editor_name_and_id == obj_in.editor_name_and_id,
            )
            .first()
        )
        if meeting_point:
            return "unchanged", obj_in
        else:
            self.create(db, obj_in=obj_in)
        return "created", obj_in

    def get_by_editor_name_and_id(
        self, db: Session, *, editor_name_and_id: str
    ) -> MeetingPoint:
        """
        Retrieve an meeting point by editor_name_and_id.

        Args:
            db (Session): The database session.
            name (str): The editor_name_and_id of the meeting point to retrieve.

        Returns:
            Optional[Editor]: The editor with the given name, or None if not found.
        """
        return (
            db.query(MeetingPoint)
            .filter(MeetingPoint.editor_name_and_id == editor_name_and_id)
            .first()
        )


meetingPoint = CRUDMeetingPoint(MeetingPoint)
