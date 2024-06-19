from typing import Any

from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse
from pydantic import Required
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import sessionmaker

from ...db.postgresdb_utils import get_database
from ...services.certified_municipality_service import (
    get_all_certified_municipalities,
    update_certified_municipality_table,
)
from ...services.meeting_point_service import get_all, update_meeting_points_table
from ..dependencies.auth_token import verify_internal_auth_token

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)


@router.get(
    "/meetingPoints",
    responses={
        200: {
            "description": "Liste des meeting points en base de données",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "city_name": "Corme-Royal",
                            "id_editor": 5,
                            "editor_name_and_id": "RDV360100358",
                            "ugf": "17046",
                        },
                        {
                            "city_name": "Huelgoat",
                            "id_editor": 2,
                            "editor_name_and_id": "Synbird2036",
                            "ugf": "29014",
                        },
                    ]
                }
            },
        }
    },
    dependencies=[Depends(verify_internal_auth_token)],
)
@limiter.limit("30/minute")
async def get_meeting_points(
    request: Request, session: sessionmaker = Depends(get_database)
) -> Any:
    """
    Récupère les données des meeting points en base de données.
    """
    try:
        return get_all(session)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while getting meeting points : {str(e)}",
        )
    finally:
        session.close()


@router.post(
    "/updateMeetingPoints",
    responses={
        200: {
            "description": "Mise à jour des meeting points effectuée avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "nb_meeting_points": 3043,
                        "created : ": "0",
                        "unchanged : ": "3043",
                    }
                }
            },
        }
    },
    dependencies=[Depends(verify_internal_auth_token)],
)
async def update_meeting_points(
    request: Request,
    uploaded_file: UploadFile = File(
        default=Required, media_type="application/vnd.ms-excel"
    ),
    session: sessionmaker = Depends(get_database),
) -> Any:
    """
    <p>
        L’API permet à l'ANTS de mettre à jour la table des meeting points.
        Le fichier Excel doit être sous la forme suivante:
        <table class="table-bordered">
            <thead>
                <tr>
                    <th>UGF/th>
                    <th>editor_name_and_id</th>
                    <th>city_name</th>
                    <th>city_name</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>{Num UGF}</td>
                    <td>{Nom éditeur concaténé avec leur id meeting point}</td>
                    <td>{Nom de la ville}</td>
                    <td>{ID de l'éditeur}</td>
                </tr>
                <tr>
                    <td>{Num UGF}</td>
                    <td>{Nom éditeur concaténé avec leur id meeting point}</td>
                    <td>{Nom de la ville}</td>
                    <td>{ID de l'éditeur}</td>
                </tr>
            </tbody>
        </table>
        </br></br>Accès via un token de sécurité unique.
    </p>
    <p>
    Règle de gestion :</br>
    <ul>
        <li>Si l'ensemble ugf et editor_name_and_id n'existe pas: un meeting point est créé en base.</li>
        <li>Sinon on le comptabilise dans les inchangés.</li>
    </ul>
    </p>
    """
    try:
        return StreamingResponse(
            content=update_meeting_points_table(session, uploaded_file),
            media_type="application/json",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error while updating meeting points",
        )
    finally:
        session.close()


@router.get(
    "/certifiedMunicipalities",
    responses={
        200: {
            "description": "Liste des mairies certifiées en base de données",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "department_code": "69",
                            "department_name": "Rhône",
                            "municipalities": [
                                {
                                    "ugf": "69080",
                                    "town_hall_name": "Mairie de COLOMBIER SAUGNIEU",
                                    "address": "14 rue de la Mairie",
                                    "zip_code": "69124",
                                    "phone_number": "04 78 32 80 17",
                                    "website": "https://www.mairie-colombiersaugnieu.fr/demarches-administratives/en-mairie/",
                                    "city_name": "COLOMBIER SAUGNIEU",
                                    "appointment_details": "Lundi : 14h – 17h\nMardi et jeudi : 9h – 12h / 14h – 18h\nMercredi : 9h – 17h\nVendredi et samedi : 9h – 12h ",
                                    "service_opening_date": "2024-03-25",
                                    "label": "sans rendez-vous",
                                    "department_code": "69",
                                    "department_name": "Rhône",
                                    "cannonized_name": "colombiersaugnieu",
                                },
                                {
                                    "ugf": "69071",
                                    "town_hall_name": "Mairie de CHASSIEU",
                                    "address": "60 rue de la République",
                                    "zip_code": "69680",
                                    "phone_number": "04 72 05 44 00",
                                    "website": "https://www.chassieu.fr/",
                                    "city_name": "CHASSIEU",
                                    "appointment_details": "Du lundi au vendredi de 08h00 à 12h00 et de 13h00 à 17h00,\nle mardi de 08h00 à 12h00 et de 14h00 à 17h00\npendant les permanences de la direction (hors vacances scolaires) :\nle mardi de 17h00 à 19h00,\nle samedi de 09h00 à 12h00",
                                    "service_opening_date": "2024-03-11",
                                    "label": "sans rendez-vous",
                                    "department_code": "69",
                                    "department_name": "Rhône",
                                    "cannonized_name": "chassieu",
                                },
                            ],
                        },
                        {
                            "department_code": "92",
                            "department_name": "Hauts-de-Seine",
                            "municipalities": [
                                {
                                    "ugf": "92040",
                                    "town_hall_name": "Mairie Annexe de CLAMART",
                                    "address": "5, rue d’Auvergne",
                                    "zip_code": "92140",
                                    "phone_number": "01 46 62 35 35",
                                    "website": "https://www.clamart.fr",
                                    "city_name": "Clamart",
                                    "appointment_details": " Les lundis, mercredis, vendredis de 8h30 à 12h30 et de 13h30 à 17h00",
                                    "service_opening_date": "2024-03-11",
                                    "label": "sans rendez-vous",
                                    "department_code": "92",
                                    "department_name": "Hauts-de-Seine",
                                    "cannonized_name": "clamart",
                                },
                            ],
                        },
                    ]
                }
            },
        }
    },
)
async def get_certified_municipalities(
    request: Request, session: sessionmaker = Depends(get_database)
) -> Any:
    """
    Récupère les données des mairies certifiées en base de données.
    """
    try:
        return get_all_certified_municipalities(session)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error while getting certified municipality : {str(e)}",
        )
    finally:
        session.close()


@router.post(
    "/updateCertifiedMunicipalities",
    responses={
        200: {
            "description": "Mise à jour des mairies certifiées effectuée avec succès",
            "content": {
                "application/json": {
                    "example": {
                        "nb_certified_municipality": 12,
                        "created : ": "12",
                        "unchanged : ": "0",
                    }
                }
            },
        }
    },
    dependencies=[Depends(verify_internal_auth_token)],
)
async def update_certified_municipalities(
    request: Request,
    uploaded_file: UploadFile = File(
        default=Required, media_type="application/vnd.ms-excel"
    ),
    session: sessionmaker = Depends(get_database),
) -> Any:
    """
    <p>
        L’API permet à l'ANTS de mettre à jour la table des mairies certifiées.
        Le fichier Excel doit être sous la forme suivante:
        <table class="table-bordered">
            <thead>
                <tr>
                    <th>Nom de la mairie</th>
                    <th>UGF</th>
                    <th>Adresse</th>
                    <th>Code postal</th>
                    <th>Ville</th>
                    <th>Téléphone</th>
                    <th>Site internet</th>
                    <th>Modalités de rendez-vous</th>
                    <th>Date d'ouverture du service</th>
                    <th>Label</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td>Mairie de CHASSIEU</td>
                    <td>69071</td>
                    <td>60 rue de la République</td>
                    <td>69680</td>
                    <td>CHASSIEU</td>
                    <td>04 72 05 44 00</td>
                    <td>https://www.chassieu.fr/</td>
                    <td>Du lundi au vendredi de 08h00 à 12h00 et de 13h00 à 17h00...</td>
                    <td>11/03/2024</td>
                    <td>sans rendez-vous</td>
                </tr>
                <tr>
                    <td>Mairie principale de CLAMART</td>
                    <td>92072</td>
                    <td>1, place Maurice Gunsbourg</td>
                    <td>92140</td>
                    <td>Clamart</td>
                    <td>01 46 62 35 35</td>
                    <td>https://www.clamart.fr</td>
                    <td>les lundis, mercredis, jeudis de 8h30 à 12h30 ...</td>
                    <td>11/03/2024</td>
                    <td>sans rendez-vous</td>
                </tr>
            </tbody>
        </table>
        </br></br>Accès via un token de sécurité unique.
    </p>
    <p>
    Règle de gestion :</br>
    <ul>
        <li>Si l'ugf n'existe pas: une entrée est créé en base.</li>
        <li>Sinon on le comptabilise dans les inchangés.</li>
    </ul>
    Il est important que chaque champ soit renseigné avec le bon format (url commençant par https:// etc...).
    </p>
    """
    try:
        return StreamingResponse(
            content=update_certified_municipality_table(session, uploaded_file),
            media_type="application/json",
        )
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Error while updating meeting points",
        )
    finally:
        session.close()
