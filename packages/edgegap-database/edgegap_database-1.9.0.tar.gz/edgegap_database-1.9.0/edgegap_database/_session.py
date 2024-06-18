import logging
from contextlib import contextmanager

from sqlmodel import Session

from ._configuration import DatabaseConfiguration
from ._engine import DatabaseEngine

logger = logging.getLogger(__name__)


class DatabaseSession:
    @staticmethod
    @contextmanager
    def get_session(configuration: DatabaseConfiguration):
        engine = DatabaseEngine(configuration).get_engine()
        session = Session(engine)

        try:
            yield session
        finally:
            session.close()
