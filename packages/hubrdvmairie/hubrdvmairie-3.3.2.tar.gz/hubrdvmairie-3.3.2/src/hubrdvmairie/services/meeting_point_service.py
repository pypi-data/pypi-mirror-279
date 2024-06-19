import io
import json
import logging
from typing import List

import xlrd
from fastapi import UploadFile
from sqlalchemy.orm import sessionmaker

from src.hubrdvmairie.models.meeting_point import MeetingPoint

from ..crud.crud_meeting_point import meetingPoint as crud

logger = logging.getLogger(__name__)


def get_all(session) -> List[MeetingPoint]:
    try:
        return crud.get_all(session)
    except Exception as e:
        logger.error("Error while getting all meeting points : %s", str(e))


def get_by_ugf(session, ugf: str) -> MeetingPoint:
    try:
        return crud.get_by_ugf(session, ugf=ugf)
    except Exception as e:
        logger.error("Error while getting meeting point by ugf : %s", str(e))


async def update_meeting_points_table(session: sessionmaker, uploaded_file: UploadFile):
    meeting_points = await read_meeting_point_from_file_streaming(uploaded_file)
    create_list = []
    unchanged_list = []
    nb_meeting_points = len(meeting_points)
    for meeting_point in meeting_points:
        res = crud.save_or_update(session, obj_in=meeting_point)
        if res[0] == "created":
            create_list.append(res[1])
        else:
            unchanged_list.append(res[1])

    yield json.dumps(
        {
            "nb_meeting_points": nb_meeting_points,
            "created : ": str(len(create_list)),
            "unchanged : ": str(len(unchanged_list)),
        }
    )


async def read_meeting_point_from_file_streaming(
    uploaded_file: UploadFile,
) -> MeetingPoint:
    # read file depending on its type
    if uploaded_file.filename.endswith(".xlsx"):
        return await read_meeting_points_file_streaming(uploaded_file)
    else:
        raise TypeError("Unknown file type : " + str(uploaded_file.filename))


async def read_meeting_points_file_streaming(uploaded_file: UploadFile):
    meeting_points = set()

    file_content = await uploaded_file.read()
    xls_data = io.BytesIO(file_content)

    workbook = xlrd.open_workbook(file_contents=xls_data.read())
    worksheet = workbook.sheet_by_index(2)

    for row_idx in range(1, worksheet.nrows):
        row = worksheet.row(row_idx)
        ugf = str(int(row[0].value))
        editor_name_and_id = row[1].value
        city_name = row[2].value
        id_editor = row[3].value

        meeting_point = MeetingPoint(
            ugf=ugf,
            editor_name_and_id=editor_name_and_id,
            city_name=city_name,
            id_editor=id_editor,
        )
        meeting_points.add(meeting_point)

    return meeting_points
