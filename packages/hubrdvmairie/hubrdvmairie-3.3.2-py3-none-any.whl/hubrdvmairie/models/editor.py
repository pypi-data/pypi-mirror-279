# pylint: disable=C0415
import asyncio
import json
import logging
import random
import threading
import time
from datetime import date, datetime, timedelta

import httpx
from dateutil import tz
from fastapi import WebSocket
from httpx import ConnectTimeout, ReadTimeout
from pydantic import ValidationError

from ..logging.app_logger import write_external_service_data
from ..models.token_ants_to_editor import TokenAntsToEditor
from ..models.token_editor_to_ants import TokenEditorToAnts
from ..services.data_validator import capitalize_custom, is_date_after_paris_datetime
from ..services.mock_data import get_mock_managed_meeting_points, get_mock_slots
from .application import Application
from .municipality import Municipality

FRA_TZ = tz.gettz("Europe/Paris")


class Editor:
    slug: str
    name: str
    url: str
    _test_mode: bool
    header_name: str
    tokens_editor_to_ants: list = [TokenEditorToAnts]
    tokens_ants_to_editor: list = [TokenAntsToEditor]
    status: bool
    api_down_datetime: datetime
    api_up_datetime: datetime
    only_connect_to_anti_duplication: bool

    def __init__(
        self,
        name: str,
        url: str,
        test_mode: bool,
        header_name: str,
        tokens_editor_to_ants: list = [TokenEditorToAnts],
        tokens_ants_to_editor: list = [TokenAntsToEditor],
        status: bool = True,
        api_down_datetime: datetime = None,
        api_up_datetime: datetime = None,
        only_connect_to_anti_duplication: bool = False,
    ):
        self.slug = name.lower().replace(" ", "-")
        self.name = name
        self.url = url
        self._test_mode = test_mode
        self.status = status
        self.api_down_datetime = api_down_datetime
        self.api_up_datetime = api_up_datetime
        self.header_name = header_name
        self.tokens_editor_to_ants = tokens_editor_to_ants
        self.tokens_ants_to_editor = tokens_ants_to_editor
        self.only_connect_to_anti_duplication = only_connect_to_anti_duplication

    async def get_managed_meeting_points(self):
        _logger = logging.getLogger("root")
        await asyncio.sleep(0.00001)
        points = []
        if self._test_mode:
            points = get_mock_managed_meeting_points(self)
        else:
            try:
                headers = {}
                headers[self.header_name] = self.tokens_ants_to_editor[0].token
                async with httpx.AsyncClient(verify=False) as async_client:
                    response = await async_client.get(
                        f"{self.url}/getManagedMeetingPoints",
                        headers=headers,
                        timeout=20,
                        follow_redirects=True,
                    )
                    write_external_service_data(
                        _logger, response, editor_name=self.name
                    )
                    if response.status_code in [200]:
                        self.api_up_datetime = datetime.now(tz=FRA_TZ)
                        if not self.status:
                            self.status = True

                        points = response.json()
                    else:
                        raise Exception(
                            f"Status code not handled : {response.status_code}"
                        )
            except Exception as get_meeting_points_e:
                if self.status:
                    self.status = False
                    self.api_down_datetime = datetime.now(tz=FRA_TZ)
                _logger.error(
                    "Error while getting meeting points",
                    extra={
                        "extra_info": {
                            "type": "app",
                            "editor_name": self.name,
                            "category": "external_service",
                            "endpoint": "getManagedMeetingPoints",
                            "error": str(get_meeting_points_e),
                        }
                    },
                )

                retry_thread = [
                    th
                    for th in threading.enumerate()
                    if th.name == f"retry-get-managed-{self.name}"
                ]
                if len(retry_thread) < 1:
                    retry_thread = threading.Thread(
                        target=self.retry_get_managed_meeting_points,
                        name=f"retry-get-managed-{self.name}",
                    )
                    retry_thread.start()

        valid_meeting_points = []
        for point in points:
            try:
                point["_editor_name"] = self.name
                point["_internal_id"] = str(point["id"])
                point["city_name"] = capitalize_custom(point["city_name"])
                if (
                    point["zip_code"]
                    and point["public_entry_address"]
                    and (point["zip_code"] in point["public_entry_address"])
                ):
                    point["public_entry_address"] = point["public_entry_address"][
                        : point["public_entry_address"].index(point["zip_code"])
                    ].strip()
                point["zip_code"] = point["zip_code"] and point["zip_code"].strip()
                Municipality.parse_obj(point)
                valid_meeting_points.append(point)
            except ValidationError as meeting_point_validation_e:
                _logger.error(
                    "Error while validating meeting point : %s \nError: %s",
                    point,
                    meeting_point_validation_e,
                    extra={"extra_info": {"type": "app", "editor_name": self.name}},
                )
            except Exception as validation_unknown_e:
                _logger.error(
                    "Error while validating meeting point : %s \nError: %s",
                    point,
                    validation_unknown_e,
                    extra={"extra_info": {"type": "app", "editor_name": self.name}},
                )

        return valid_meeting_points

    async def get_available_time_slots(
        self, meeting_points, start_date, end_date, reason="CNI", documents_number=1
    ):
        _logger = logging.getLogger("root")
        # this sleep is necessary to not block other async operations
        await asyncio.sleep(0.00001)
        result = {}
        editor_error = None
        response = None

        def last_day_of_month(any_day):
            next_month = any_day.replace(day=28) + timedelta(days=4)
            return (next_month.replace(day=1) - timedelta(days=1)).day

        # start_date and end_date should be fixed to help editors handle their cache
        monthly_start_date = None
        monthly_end_date = None
        try:
            monthly_start_date = start_date.replace(
                day=date.today().day if start_date.month == date.today().month else 1
            )
            monthly_end_date = end_date.replace(day=last_day_of_month(end_date))
        except Exception as monthly_date_e:
            _logger.error(
                "Error while creating monthly search dates: %s",
                monthly_date_e,
                extra={"extra_info": {"type": "app"}},
            )

        if self._test_mode:
            await asyncio.sleep(random.randint(3, 12))
            for meeting_point in meeting_points:
                meeting_point_slots = get_mock_slots(
                    meeting_point, start_date, end_date
                )
                result[meeting_point["_internal_id"]] = meeting_point_slots
        else:
            meeting_point_ids = [x["_internal_id"] for x in meeting_points]
            try:
                headers = {}
                headers[self.header_name] = self.tokens_ants_to_editor[0].token
                parameters = {
                    "start_date": start_date or monthly_start_date or date.today(),
                    "end_date": end_date
                    or monthly_end_date
                    or (date.today() + timedelta(days=150)),
                    "meeting_point_ids": meeting_point_ids,
                    "reason": reason,
                    "documents_number": documents_number,
                }
                async with httpx.AsyncClient(verify=False) as async_client:
                    response = await async_client.get(
                        f"{self.url}/availableTimeSlots",
                        headers=headers,
                        params=parameters,
                        timeout=15,
                        follow_redirects=True,
                    )
                    write_external_service_data(_logger, response, self.name)
                    if response.status_code in [200]:
                        self.api_up_datetime = datetime.now(tz=FRA_TZ)
                        if not self.status:
                            self.status = True
                            self.api_down_datetime = datetime.now(tz=FRA_TZ)

                        result = response.json()
                    else:
                        raise Exception(
                            f"Status code not handled : {response.status_code} : {response.reason_phrase}"
                        )
            except ReadTimeout:
                if self.status:
                    self.status = False
                    self.api_down_datetime = datetime.now(tz=FRA_TZ)

                _logger.error(
                    "Timeout while getting available time slots for %s",
                    self.name,
                    extra={
                        "extra_info": {
                            "type": "app",
                            "editor_name": self.name,
                            "category": "external_service",
                            "endpoint": "availableTimeSlots",
                        }
                    },
                )
            except ConnectTimeout:
                if self.status:
                    self.status = False
                    self.api_down_datetime = datetime.now(tz=FRA_TZ)

                _logger.error(
                    "Connexion Timeout while getting available time slots for %s",
                    self.name,
                    extra={
                        "extra_info": {
                            "type": "app",
                            "editor_name": self.name,
                            "category": "external_service",
                            "endpoint": "availableTimeSlots",
                        }
                    },
                )
            except Exception as available_time_slots_e:
                if self.status:
                    self.status = False
                    self.api_down_datetime = datetime.now(tz=FRA_TZ)

                _logger.error(
                    "Error while getting available time slots for %s : %s",
                    self.name,
                    str(available_time_slots_e),
                    extra={
                        "extra_info": {
                            "type": "app",
                            "parameters": {
                                "start_date": str(parameters["start_date"]),
                                "end_date": str(parameters["end_date"]),
                                "meeting_point_ids": parameters["meeting_point_ids"],
                                "reason": parameters["reason"],
                                "documents_number": parameters["documents_number"],
                            },
                            "editor_name": self.name,
                            "category": "external_service",
                            "endpoint": "availableTimeSlots",
                        }
                    },
                )
                editor_error = {"error": available_time_slots_e, "editor": self.name}

        if (not start_date) and (not end_date):
            return result, None

        filtered_dates_result = {}
        try:
            for meeting_point_id in result:
                filtered_dates_result[meeting_point_id] = []
                for available_timeslot in result[meeting_point_id]:
                    timeslot_datetime = None
                    for datetime_format in ["%Y-%m-%dT%H:%MZ", "%Y-%m-%dT%H:%M:%S%z"]:
                        try:
                            timeslot_datetime = datetime.strptime(
                                available_timeslot["datetime"], datetime_format
                            )

                            if timeslot_datetime.tzinfo:
                                utcoffset = (
                                    timeslot_datetime.utcoffset().total_seconds()
                                    / 60
                                    / 60
                                )
                                timeslot_datetime = timeslot_datetime.replace(
                                    tzinfo=None
                                ) + timedelta(hours=utcoffset)

                            break
                        except ValueError:
                            pass
                    if (
                        (not timeslot_datetime)
                        or (start_date and (timeslot_datetime.date() < start_date))
                        or (end_date and (timeslot_datetime.date() > end_date))
                        or (is_date_after_paris_datetime(timeslot_datetime))
                    ):
                        message = "DATE OUT OF RANGE"
                        if is_date_after_paris_datetime(timeslot_datetime):
                            message = "DATE IN THE PAST"
                        _logger.debug(
                            "[%s] %s : %s",
                            self.name,
                            message,
                            str(timeslot_datetime),
                        )
                    else:
                        filtered_dates_result[meeting_point_id].append(
                            {
                                "datetime": timeslot_datetime.strftime(
                                    "%Y-%m-%dT%H:%M:%SZ"
                                ),
                                "callback_url": available_timeslot["callback_url"],
                            }
                        )
        except Exception as checking_date_filter_e:
            _logger.error(
                "[%s] Checking date filter error : %s",
                self.name,
                str(checking_date_filter_e),
                extra={"extra_info": {"type": "app", "editor_name": self.name}},
            )
            editor_error = {"error": checking_date_filter_e, "editor": self.name}
        return filtered_dates_result, editor_error

    async def search_slots_in_editor(
        self,
        meeting_points,
        start_date,
        end_date,
        reason="CNI",
        documents_number=1,
        websocket: WebSocket = None,
    ):
        # this sleep is necessary to not block other async operations
        time.sleep(0.00001)
        editor_error = None
        editor_meeting_points = []
        editor_meeting_points_with_slots = []
        for meeting_point in meeting_points:
            if meeting_point["_editor_name"] == self.name:
                editor_meeting_points.append(meeting_point)
        if editor_meeting_points:
            slots, editor_error = await self.get_available_time_slots(
                editor_meeting_points, start_date, end_date, reason, documents_number
            )
            for meeting_point in editor_meeting_points:
                if (
                    meeting_point["_internal_id"] in slots
                    and slots[meeting_point["_internal_id"]]
                ):
                    meeting_point["available_slots"] = slots[
                        meeting_point["_internal_id"]
                    ]
                    editor_meeting_points_with_slots.append(meeting_point)
            if websocket:
                safe_editor_meeting_points_with_slots = []
                for editor_meeting_point_with_slots in editor_meeting_points_with_slots:
                    editor_meeting_point_with_slots_copy = (
                        editor_meeting_point_with_slots.copy()
                    )
                    if "_editor_name" in editor_meeting_point_with_slots_copy:
                        del editor_meeting_point_with_slots_copy["_editor_name"]
                    if "_internal_id" in editor_meeting_point_with_slots_copy:
                        del editor_meeting_point_with_slots_copy["_internal_id"]
                    safe_editor_meeting_points_with_slots.append(
                        editor_meeting_point_with_slots_copy
                    )
                json_string = json.dumps(
                    safe_editor_meeting_points_with_slots, default=str
                )
                await websocket.send_text(json_string)
        return editor_meeting_points_with_slots, editor_error

    async def search_meetings(self, application_ids):
        _logger = logging.getLogger("root")
        await asyncio.sleep(0.00001)
        meetings = {}
        if not self._test_mode:
            try:
                headers = {}
                headers[self.header_name] = self.tokens_ants_to_editor[0].token
                parameters = {"application_ids": application_ids}
                async with httpx.AsyncClient(verify=False) as async_client:
                    response = await async_client.get(
                        f"{self.url}/searchApplicationIds",
                        headers=headers,
                        params=parameters,
                        timeout=5,
                        follow_redirects=True,
                    )
                    write_external_service_data(_logger, response, self.name)
                    if response.status_code in [200]:
                        meetings = response.json()
                    else:
                        raise Exception(
                            f"Status code not handled : {response.status_code} : {response.reason_phrase}"
                        )
            except Exception as search_meetings_e:
                _logger.error(
                    "Error while seachring meetings by application ID for %s : %s",
                    self.name,
                    str(search_meetings_e),
                    extra={"extra_info": {"type": "app", "editor_name": self.name}},
                )
        else:
            await asyncio.sleep(random.randint(3, 5))

        valid_meetings = {}
        for applicationId in meetings:
            valid_meetings[applicationId] = []
            for meeting in meetings[applicationId]:
                try:
                    Application.parse_obj(meeting)
                    valid_meetings[applicationId].append(meeting)
                except ValidationError as meeting_validation_e:
                    _logger.error(
                        "Error while validating meeting : %s \nError: %s",
                        meeting,
                        meeting_validation_e,
                        extra={"extra_info": {"type": "app", "editor_name": self.name}},
                    )
        return valid_meetings

    def retry_get_managed_meeting_points(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        result = loop.run_until_complete(self._retry_get_managed_meeting_points())
        loop.close()

        return result

    async def _retry_get_managed_meeting_points(self):
        _logger = logging.getLogger("root")

        counter = 0
        while counter < 60 * 20:
            time.sleep(1 * 60)
            try:
                meeting_points = await self.get_managed_meeting_points()
                if meeting_points:
                    from unidecode import unidecode

                    from ..db.utils import (
                        get_all_meeting_points,
                        set_all_meeting_points,
                    )

                    all_meeting_points = get_all_meeting_points()

                    point_index = len(all_meeting_points) + 1
                    for point in meeting_points:
                        point["id"] = str(point_index)
                        point["decoded_city_name"] = (
                            unidecode(point["city_name"])
                            .replace(" ", "-")
                            .replace("'", "-")
                            .lower()
                        )
                        point_index += 1

                    all_meeting_points += meeting_points
                    set_all_meeting_points(all_meeting_points)
                    break
                else:
                    raise Exception(f"No meeting points found for editor {self.name}")
            except Exception as retry_get_managed_meeting_points_e:
                _logger.error(
                    "Error while retrying to get managed meeting for editor %s : %s",
                    self.name,
                    retry_get_managed_meeting_points_e,
                    extra={"extra_info": {"type": "app"}},
                )
            counter += 1

        _logger.info(
            "End of retrying to get managed meeting points for editor %s",
            self.name,
            extra={"extra_info": {"type": "app"}},
        )

    def convert_to_front(self):
        return {
            "slug": self.slug,
            "name": self.name,
            "status": self.status,
            "api_down_datetime": self.api_down_datetime,
            "api_up_datetime": self.api_up_datetime,
        }


def init_all_editors():
    from ..crud.crud_editor import editor as crud
    from ..db.postgresdb import session

    try:
        editors = crud.get_editors_not_only_opti(db=session)
        editors_list = []
        if editors:
            for editor in editors:
                dto = editor.to_dto()
                editors_list.append(dto)
        else:
            print("No editors found in database")
        print("------- Done loading editors -------")
        return editors_list
    except Exception as e:
        print("Error while getting editors : ", str(e))
    finally:
        session.close()
