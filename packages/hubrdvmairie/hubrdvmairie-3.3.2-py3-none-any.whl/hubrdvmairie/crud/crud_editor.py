from typing import List, Optional

from sqlalchemy.orm import Session

from ..crud.base import CRUDBase
from ..models.editor_model import Editor
from ..schemas.editor import EditorCreate, EditorUpdate


class CRUDEditor(CRUDBase[Editor, EditorCreate, EditorUpdate]):
    """
    CRUD operations for the Editor model.
    """

    def get_by_name(self, db: Session, *, name: str) -> Optional[Editor]:
        """
        Retrieve an editor by name.

        Args:
            db (Session): The database session.
            name (str): The name of the editor to retrieve.

        Returns:
            Optional[Editor]: The editor with the given name, or None if not found.
        """
        return db.query(Editor).filter(Editor.name == name).first()

    def get_all(self, db: Session) -> List[Editor]:
        """
        Retrieve all editors.

        Args:
            db (Session): The database session.

        Returns:
            List[Editor]: A list of all editors.
        """
        return db.query(Editor).all()

    def get_by_token(self, db: Session, *, token: str) -> Optional[Editor]:
        """
        Retrieve an editor by token.

        Args:
            db (Session): The database session.
            token (str): The token of the editor to retrieve.

        Returns:
            Optional[Editor]: The editor with the given token, or None if not found.
        """
        return (
            db.query(Editor)
            .filter(Editor.tokens_editor_to_ants.any(token=token))
            .first()
        )

    def get_editors_not_only_opti(self, db: Session) -> List[Editor]:
        """
        Retrieve a list of editors that are not only connected to anti-duplication.

        Args:
            db (Session): The database session.

        Returns:
            List[Editor]: A list of Editor objects.
        """
        return db.query(Editor).filter_by(only_connect_to_anti_duplication=False).all()


editor = CRUDEditor(Editor)
