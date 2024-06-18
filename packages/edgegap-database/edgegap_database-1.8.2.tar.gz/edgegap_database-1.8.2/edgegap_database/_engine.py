from sqlalchemy.engine import Engine
from sqlmodel import create_engine

from ._configuration import DatabaseConfiguration


class DatabaseEngine:
    __mapping__: dict[str, '__Engine'] = {}
    __instance: '__Engine'

    class __Engine:
        def __init__(self, configuration: DatabaseConfiguration):
            self.__configuration = configuration
            self.__engine = create_engine(
                url=str(self.__configuration.uri),
                connect_args=self.__configuration.args or {},
                poolclass=self.__configuration.pool_class or None,
            )

        def get_engine(self):
            return self.__engine

    def __init__(self, configuration: DatabaseConfiguration):
        key = configuration.application

        if key not in DatabaseEngine.__mapping__:
            DatabaseEngine.__mapping__[key] = self.__Engine(configuration)

        self.__key = key

    def get_engine(self) -> Engine:
        instance: DatabaseEngine.__Engine = DatabaseEngine.__mapping__.get(self.__key)

        return instance.get_engine()
