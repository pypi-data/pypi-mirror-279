import asyncio
import os
from datetime import date
from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from markdown import markdown
from pydantic import Required
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import sessionmaker

from ...db.postgresdb_utils import get_database
from ...db.utils import (
    get_all_editors,
    get_all_meeting_points,
    get_all_offline_meeting_points,
)
from ...models.announcement import Announcement
from ...models.municipality import (
    Municipality,
    MunicipalityWithDistance,
    OfflineMunicipality,
    OfflineMunicipalityWithDistance,
)
from ...services.panorama_service import get_all_editor_panorama
from ...services.search_meeting_points import (
    search_close_meeting_points,
    search_close_offline_meeting_points,
)
from ..dependencies.auth_token import verify_internal_auth_token

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/MeetingPointsFromPosition",
    response_model=List[MunicipalityWithDistance],
    responses={
        200: {
            "description": "Les Meetings points ont bien été trouvés",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "201",
                            "name": "Mairie ANNEXE LILLE-SECLIN",
                            "longitude": 3.0348016639327,
                            "latitude": 50.549140395451,
                            "public_entry_address": "89 RUE ROGER BOUVRY",
                            "zip_code": "59113",
                            "city_name": "SECLIN",
                            "website": "https://www.ville-seclin.fr",
                            "city_logo": "https://www.ville-seclin.fr/images/logo-ville-seclin/logo_ville_de_seclin.png",
                            "distance_km": 1.56,
                        }
                    ]
                }
            },
        }
    },
)
@limiter.limit("30/minute")
def meeting_points_from_position(
    request: Request,
    longitude: float = Query(default=Required, example=2.352222),
    latitude: float = Query(default=Required, example=48.856613),
    radius_km: int = Query(default=20, enum=[20, 40, 60]),
) -> List[MunicipalityWithDistance]:
    """
    Recherche des meeting points à partir d'une coordonnée GPS.
    """
    all_points: List[Municipality] = get_all_meeting_points()
    meeting_points: List[MunicipalityWithDistance] = search_close_meeting_points(
        all_points, latitude, longitude, radius_km
    )
    return meeting_points


@router.get(
    "/Announcement",
    response_model=Announcement,
    responses={
        200: {
            "description": "System global announcement",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "title": "Alerte de sécurité",
                            "description": "Attention, le site rencontre des attaques recurrentes en ce moment.",
                            "alert_level": "error",
                        }
                    ]
                }
            },
        }
    },
)
@limiter.limit("30/minute")
def global_announcement(request: Request) -> Any:
    """
    Retourne un objet d'annonce globale.
    """
    if (
        ("ANNOUNCEMENT_TITLE" in os.environ)
        and ("ANNOUNCEMENT_DESCRIPTION" in os.environ)
        and ("ANNOUNCEMENT_ALERT_LEVEL" in os.environ)
    ):
        return {
            "title": os.environ.get("ANNOUNCEMENT_TITLE"),
            "description": markdown(os.environ.get("ANNOUNCEMENT_DESCRIPTION")),
            "alert_level": os.environ.get("ANNOUNCEMENT_ALERT_LEVEL"),
        }
    return Response(status_code=200)


@router.get(
    "/searchCity",
    response_model=Municipality,
    responses={
        200: {
            "description": "La ville a bien été trouvée",
            "content": {
                "application/json": {
                    "example": {
                        "id": "201",
                        "name": "Annexe mairie des Favignolles à Romorantin",
                        "longitude": 1.751597,
                        "latitude": 47.349797,
                        "public_entry_address": "1 rue François RABELAIS",
                        "zip_code": "41200",
                        "city_name": "Romorantin-Lanthenay",
                        "decoded_city_name": "romorantin-lanthenay",
                        "website": "https://rendezvousonline.fr/alias/romorantin-lanthenay-41200-2",
                        "city_logo": "https://pro.rendezvousonline.fr/upload/account/image/logo/2G8VjHfrJWB93mYFhPiYO5F4bPRJdaJz.jpg",
                    }
                }
            },
        }
    },
)
@limiter.limit("30/minute")
def search_city(
    request: Request,
    name: str = Query(default=Required, example="romorantin-lanthenay"),
) -> Municipality:
    """
    Recherche les meeting points d'une ville.
    """
    all_points: List[Municipality] = get_all_meeting_points()
    city = None
    if name == "lyon":
        for point in all_points:
            if point["name"] == "Mairie du 3ème arrondissement":
                city = point
                return city
    elif name == "paris":
        for point in all_points:
            if point["name"] == "Service titres d'identité de Paris  Centre":
                city = point
                return city
    elif name == "marseille":
        for point in all_points:
            if point["name"] == "Mairie de Marseille : BMdP Désirée Clary":
                city = point
                return city
    else:
        for point in all_points:
            if point["decoded_city_name"] == name:
                city = point
                return city
    return city


@router.get(
    "/status",
    responses={
        200: {
            "description": "Informations des éditeurs",
            "content": {
                "application/json": {
                    "example": {
                        "editors": [
                            {
                                "slug": "troov",
                                "name": "Troov",
                                "api_url": "https://qa-api.troov.com/api",
                                "status": True,
                            }
                        ]
                    }
                }
            },
        }
    },
)
@limiter.limit("30/minute")
async def get_editors(request: Request) -> Any:
    """
    Donne les détails des éditeurs.
    """
    all_editors = get_all_editors()
    editors = []
    for editor in all_editors:
        editors.append(editor.convert_to_front())
    return {"editors": editors}


@router.get(
    "/searchOfflineMeetingPoints",
    response_model=List[OfflineMunicipalityWithDistance],
    responses={
        200: {
            "description": "La recherche des meeting points hors ligne a bien aboutie",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": "201",
                            "nmunicipality": "Paris 10",
                            "public_entry_address": "72 Rue du Faubourg Saint-Martin",
                            "phone_number": "04 14 04 44 44",
                            "decoded_city_name": "paris",
                            "url": "https://urldumeetingpoint.fr",
                            "logo": "https://urldulogo.fr",
                            "website": "https://mairie10.paris.fr",
                            "distance_km": 1.56,
                        }
                    ]
                }
            },
        }
    },
)
@limiter.limit("30/minute")
def search_offline_meeting_points(
    request: Request,
    longitude: float = Query(default=Required, example=2.352222),
    latitude: float = Query(default=Required, example=48.856613),
    radius_km: float = Query(default=20, enum=[0.99, 5, 10, 15, 20, 25, 30]),
) -> List[OfflineMunicipalityWithDistance]:
    """
    Recherche des meeting points hors ligne autour d'une position GPS
    """
    all_offline_points: List[OfflineMunicipality] = get_all_offline_meeting_points()
    meeting_points: List[
        OfflineMunicipalityWithDistance
    ] = search_close_offline_meeting_points(
        all_offline_points, latitude, longitude, radius_km
    )
    return meeting_points


@router.get(
    "/internalAvailableTimeSlots",
    include_in_schema=False,
    responses={
        200: {
            "description": "Les rendez-vous disponibles pour les meeting points id ont bien été trouvés",
            "content": {
                "application/json": {
                    "example": {
                        "506": [
                            {
                                "datetime": "2022-12-19T10:00Z",
                                "callback_url": "https://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T10:00Z",
                            },
                            {
                                "datetime": "2022-12-19T10:20Z",
                                "callback_url": "https://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T10:20Z",
                            },
                            {
                                "datetime": "2022-12-19T10:40Z",
                                "callback_url": "https://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T10:40Z",
                            },
                            {
                                "datetime": "2022-12-19T11:00Z",
                                "callback_url": "https://www.ville-seclin.fr/rendez-vous/passeports?date=2022-12-19T11:00Z",
                            },
                        ],
                        "7789": [
                            {
                                "datetime": "2022-12-19T10:00Z",
                                "callback_url": "https://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T10:00Z",
                            },
                            {
                                "datetime": "2022-12-19T10:20Z",
                                "callback_url": "https://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T10:20Z",
                            },
                            {
                                "datetime": "2022-12-19T10:40Z",
                                "callback_url": "https://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T10:40Z",
                            },
                            {
                                "datetime": "2022-12-19T11:00Z",
                                "callback_url": "https://www.lille.fr/Lille-Sud2/Mairie-de-quartier-de-Lille-Sud/rendez-vous/passeports?date=2022-12-19T11:00Z",
                            },
                        ],
                    }
                }
            },
        },
        "401": {
            "description": "Utilisateur non autorisé",
            "content": {
                "application/json": {"example": "X-HUB-RDV-AUTH-TOKEN header invalid"}
            },
        },
        "404": {
            "description": "Meeting point id non trouvé",
            "content": {
                "application/json": {"example": "Unknown Meeting Point ID : 11TEST2111"}
            },
        },
    },
    dependencies=[Depends(verify_internal_auth_token)],
)
async def get_available_time_slots(
    request: Request,
    meeting_point_ids: list[str] = Query(default=Required, example=["201", "203"]),
    start_date: date = Query(default=Required, example="2022-11-01"),
    end_date: date = Query(default=Required, example="2022-11-30"),
    reason: str = Query(default="CNI", enum=["CNI", "PASSPORT", "CNI-PASSPORT"]),
    documents_number: int = Query(default=1),
):
    """
    Récupère les rendez-vous disponibles sur une période donnée pour une liste de meeting point id.
    <br>
    Attention: L'heure qui sera affichée est l'heure exacte que l'on trouve dans la réponse.
    """

    all_points = get_all_meeting_points()

    result = {}

    meeting_points = []
    for meeting_point_id in meeting_point_ids:
        meeting_point = None
        index = 0
        while index < len(all_points):
            if meeting_point_id == all_points[index]["id"]:
                meeting_point = all_points[index]
                break
            index += 1

        if not meeting_point:
            raise HTTPException(
                status_code=404, detail=f"Unknown Meeting Point ID : {meeting_point_id}"
            )
        meeting_points.append(meeting_point)
    editor_futures = []
    for editor in get_all_editors():
        editor_futures.append(
            asyncio.ensure_future(
                editor.search_slots_in_editor(
                    meeting_points,
                    start_date,
                    end_date,
                    reason,
                    documents_number,
                    None,
                )
            )
        )
    all_editor_time_slots = await asyncio.gather(*editor_futures)
    for editor_time_slots in all_editor_time_slots:
        for meeting_point_slots in editor_time_slots[0]:
            result[meeting_point_slots["id"]] = meeting_point_slots["available_slots"]

    return result


@router.get(
    "/panorama",
    responses={
        200: {
            "description": "Panorama des éditeurs",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "site_url": "https://www.urlDeLediteurconcerne.fr/",
                            "overseas": False,
                            "limit_appointment_outside": True,
                            "use_queue": False,
                            "is_connect_to_anti_duplication": True,
                            "contact_url": "https://www.urlDeLediteurconcerne.fr/contact",
                            "name": "Nom de l'editeur",
                            "logo_url": "https://www.urlDeLediteurconcerne.fr/logo.png",
                            "integration_predemande": True,
                            "saas": True,
                            "is_connect_to_hub": True,
                        },
                    ]
                }
            },
        }
    },
)
@limiter.limit("30/minute")
async def get_editors_panorama(
    request: Request, session: sessionmaker = Depends(get_database)
) -> Any:
    """
    Récupère les données des éditeurs de la page panorama

    Retourne:
        La liste de tous les éditeurs.
    """
    try:
        all_editors = get_all_editor_panorama(session)
        return all_editors
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while getting editors panorama : {str(e)}",
        )
    finally:
        session.close()
