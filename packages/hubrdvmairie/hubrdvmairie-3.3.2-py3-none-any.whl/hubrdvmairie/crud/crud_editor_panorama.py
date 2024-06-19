from typing import List, Optional

from sqlalchemy.orm import Session

from ..crud.base import CRUDBase
from ..models.editor_panorama import EditorPanorama
from ..schemas.editor_panorama import EditorPanoramaCreate, EditorPanoramaUpdate


class CRUDEditorPanorama(
    CRUDBase[EditorPanorama, EditorPanoramaCreate, EditorPanoramaUpdate]
):
    """
    CRUD operations for the Editor model.
    """

    def get_by_name(self, db: Session, *, name: str) -> Optional[EditorPanorama]:
        """
        Retrieve an editor by name.

        Args:
            db (Session): The database session.
            name (str): The name of the editor to retrieve.

        Returns:
            Optional[Editor]: The editor with the given name, or None if not found.
        """
        return db.query(EditorPanorama).filter(EditorPanorama.name == name).first()

    def get_all(self, db: Session) -> List[EditorPanorama]:
        """
        Retrieve all editors.

        Args:
            db (Session): The database session.

        Returns:
            List[Editor]: A list of all editors.
        """
        return db.query(EditorPanorama).all()


editorPanorama = CRUDEditorPanorama(EditorPanorama)
