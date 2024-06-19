import logging
from typing import List

from src.hubrdvmairie.models.editor_panorama import EditorPanorama

from ..crud.crud_editor_panorama import editorPanorama as crud

logger = logging.getLogger(__name__)


def get_all_editor_panorama(session) -> List[EditorPanorama]:
    try:
        return crud.get_all(session)
    except Exception as e:
        logger.error("Error while getting all editor panorama : %s", str(e))
