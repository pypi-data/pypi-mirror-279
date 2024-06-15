from contextlib import contextmanager
from pystacho.helper import Helper
from pystacho.config import Config
from pystacho.adapters.mysql import Mysql
from pystacho.adapters.sqlite import Sqlite
from pystacho.adapters.postgres import Postgres
from pystacho.query_builder import QueryBuilder


class Database(QueryBuilder):
    def __init__(self):
        self._config = None
        self._adapter = None
        self.setup()

        super().__init__(self._adapter)

    def setup(self):
        # if self.config is None or self.adapter is None:
        self._config = Config()
        self._adapter = self.setup_adapter()

    def setup_adapter(self):
        if self._config.adapter_name() == "mysql":
            return Mysql(self._config.database_config())
        elif self._config.adapter_name() == "sqlite":
            return Sqlite(self._config.database_config())
        elif self._config.adapter_name() == "postgres":
            return Postgres(self._config.database_config())
        else:
            raise ValueError("Invalid adapter.")

    @contextmanager
    def database_connection(self):
        self.setup()

        with self._adapter.database_connection() as connection:
            yield connection
