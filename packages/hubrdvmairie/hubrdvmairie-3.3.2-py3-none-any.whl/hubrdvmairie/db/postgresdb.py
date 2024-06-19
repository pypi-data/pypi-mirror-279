"""
This module contains the code for creating a PostgreSQL database connection and session.

Functions:
- check_database: checks if the database exists, and creates it if it doesn't.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker
from sqlalchemy_utils import create_database, database_exists

from ..core.config import get_settings


def check_database():
    """
    Checks if the database exists, and creates it if it doesn't.
    """
    if not database_exists(get_settings().database_url):
        create_database(get_settings().database_url)


engine = create_engine(
    get_settings().database_url,
    pool_size=5,
    max_overflow=2,
    echo=False,
    pool_pre_ping=True,
)

session: scoped_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

Base = declarative_base()
