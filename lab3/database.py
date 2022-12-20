from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


class DataBase:

    def __init__(self):
        self.connection = None
        self.engine = None

    def connect(self, db_url: str) -> None:
        """Установка соединения с БД."""
        self.engine = create_engine(db_url)
        self.connection = self.engine.connect()

    def get_session(self) -> Session:
        """Выдача сессии."""
        session = scoped_session(sessionmaker(autoflush=True, bind=self.engine))
        return session

    def close_connect(self) -> None:
        """Отключение соединения с БД."""
        if self.connection:
            self.connection.close()
