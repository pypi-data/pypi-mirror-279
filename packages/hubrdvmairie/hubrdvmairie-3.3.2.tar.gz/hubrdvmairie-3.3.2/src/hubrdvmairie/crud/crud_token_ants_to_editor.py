from typing import Optional

from sqlalchemy.orm import Session

from ..crud.base import CRUDBase
from ..models.token_ants_to_editor import TokenAntsToEditor
from ..schemas.token_ants_to_editor import (
    TokenAntsToEditorCreate,
    TokenAntsToEditorUpdate,
)


class CRUDTokenAntsToEditor(
    CRUDBase[TokenAntsToEditor, TokenAntsToEditorCreate, TokenAntsToEditorUpdate]
):
    """
    CRUD operations for TokenAntsToEditor model.
    """

    def get_by_token(self, db: Session, *, token: str) -> Optional[TokenAntsToEditor]:
        """
        Retrieve a token by its value.

        Args:
            db (Session): The database session.
            token (str): The token value.

        Returns:
            Optional[TokenAntsToEditor]: The token if found, None otherwise.
        """
        return (
            db.query(TokenAntsToEditor).filter(TokenAntsToEditor.token == token).first()
        )

    def get_all(self, db: Session):
        """
        Returns all TokenAntsToEditor objects from the database.

        Args:
        - db: SQLAlchemy Session instance.

        Returns:
        - List of TokenAntsToEditor objects.
        """
        return db.query(TokenAntsToEditor).all()

    def get_by_editor_id(
        self, db: Session, *, editor_id: int
    ) -> Optional[TokenAntsToEditor]:
        """
        Retrieve a token for a given editor_id.

        Args:
            db (Session): The database session.
            editor_id (int): The ID of the editor.

        Returns:
            Optional[TokenAntsToEditor]: The token for the given editor_id, if it exists.
        """
        return (
            db.query(TokenAntsToEditor)
            .filter(TokenAntsToEditor.editor_id == editor_id)
            .first()
        )


token_ants_to_editor = CRUDTokenAntsToEditor(TokenAntsToEditor)
