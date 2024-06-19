from typing import List, Optional

from sqlalchemy.orm import Session

from ..crud.base import CRUDBase
from ..models.token_editor_to_ants import TokenEditorToAnts
from ..schemas.token_editor_to_ants import (
    TokenEditorToAntsCreate,
    TokenEditorToAntsUpdate,
)


class CRUDTokenEditorToAnts(
    CRUDBase[TokenEditorToAnts, TokenEditorToAntsCreate, TokenEditorToAntsUpdate]
):
    """
    CRUD operations for TokenEditorToAnts model.
    """

    def get_by_token(self, db: Session, *, token: str) -> Optional[TokenEditorToAnts]:
        """
        Retrieve a token by its value.

        Args:
            db (Session): SQLAlchemy session object.
            token (str): Token value.

        Returns:
            Optional[TokenEditorToAnts]: TokenEditorToAnts object if found, else None.
        """
        return (
            db.query(TokenEditorToAnts).filter(TokenEditorToAnts.token == token).first()
        )

    def get_all(self, db: Session):
        """
        Retrieve all tokens.

        Args:
            db (Session): SQLAlchemy session object.

        Returns:
            List[TokenEditorToAnts]: List of all TokenEditorToAnts objects.
        """
        return db.query(TokenEditorToAnts).all()

    def get_valid_token(self, db: Session) -> List[TokenEditorToAnts]:
        """
        Retrieve all tokens.

        Args:
            db (Session): SQLAlchemy session object.

        Returns:
            List[TokenEditorToAnts]: List of all TokenEditorToAnts objects.
        """
        tokens: List[TokenEditorToAnts] = db.query(TokenEditorToAnts).all()
        valid_token = [token for token in tokens if token.is_valid()]
        return valid_token


tokenEditorToAnts = CRUDTokenEditorToAnts(TokenEditorToAnts)
