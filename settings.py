from os import environ
from typing import Tuple, Type

from logging import getLogger
from logging.config import dictConfig
import json

from configparser import ConfigParser

from classes.server import Server
from classes.backed_connectors import SQLDB, NoSQLDB
from classes.model import Patterns

from logging import getLogger

class Setup:
    ''' Setting up application classes '''

    @classmethod
    async def setup(cls):
        ''' Apply settings '''
        s = Setup()
        log_path_file, app_path_file = s._get_ini_files()

        s._set_logging(path=log_path_file)
        s._read_app_config(path=app_path_file)

        s._setup_server()
        s._setup_sql_db()
        await s._setup_no_sql_db()
        s._setup_patterns()
        return 0

    def _set_logging(self, path: str) -> int:
        ''' Setting of application logger '''
        with open(path, 'r') as logging_configuration_file:  
            config_dict = json.load(logging_configuration_file, strict=False)
            dictConfig(config_dict)

        logger = getLogger(__name__)
        logger.debug("*"*100 + "\n")
        logger.debug("start setup...")
        return 0
        
    def _get_ini_files(self) -> Tuple[str, str]:
        ''' Getting of ini-files '''
        log_setting = environ.get("log_setting")
        app_setting = environ.get("app_setting")
        return log_setting, app_setting

    def _read_app_config(self, path: str) -> int:
        ''' Read application config file '''
        self._config = ConfigParser()
        self._config.read(path, encoding="UTF-8")
        return 0

    def _setup_server(self) -> int:
        '''  '''
        Server.set_cls_params(
            host=self._config["SERVER"]["host"],
            port=self._config["SERVER"]["port"],
        )
        return 0

    def _setup_sql_db(self) -> int:
        '''  '''
        sqldb = SQLDB(
            params=dict(
                connection_string=self._config["SQL_DB"]["connection_string"],
                pool_size=int(self._config["SQL_DB"]["pool_size"]),
                max_overflow=int(self._config["SQL_DB"]["max_overflow"])
            )
        )
        return 0

    async def _setup_no_sql_db(self) -> int:
        '''  '''
        await NoSQLDB.init(
            params=dict(
                connection_string=self._config["NO_SQL_DB"]["connection_string"],
                minsize=int(self._config["NO_SQL_DB"]["minsize"]),
                maxsize=int(self._config["NO_SQL_DB"]["maxsize"])
            )
        )
        return 0

    def _setup_patterns(self) -> int:
        '''  '''
        Patterns.set_cls_params(
            update_delay=int(self._config["PATTERNS"]["update_delay"])
        )
        return 0