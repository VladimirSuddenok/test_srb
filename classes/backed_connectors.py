from sqlalchemy import text, pool
from sqlalchemy.ext.asyncio import create_async_engine
import aioredis
from typing import Type, Dict, Union, List
from sqlalchemy.engine.cursor import CursorResult
from classes.parents_classes.base_class import debug_logger_inst, debug_logger

from logging import getLogger
from os import environ

logger = getLogger(__name__)

# types
db_record = Dict[str, Union[int, str]]
db_answer = List[db_record]
init_params = Dict[str, Union[int, str]]

class SQLDB:
    ''' Class relation db connectors '''

    query_get_patterns = 'select * from patterns;'

    @debug_logger_inst
    def __init__(self, params: init_params = {}):
        ''' Constructor '''
        if params:
            self._pool = create_async_engine(
                params["connection_string"],
                poolclass=pool.QueuePool,
                pool_size=params["pool_size"],
                max_overflow=params["max_overflow"]
            )

    def __new__(cls, *args, **kwargs) -> Type["SQLDB"]:
        ''' Pattern singleton '''
        if not hasattr(cls, 'instance'):
            cls.instance = super(SQLDB, cls).__new__(cls)
        return cls.instance
    
    async def _execute_query(self, query: str) -> db_answer:
        '''  '''
        async with self._pool.begin() as conn:
            result = await conn.execute(text(query))
            return await self._cursor2dict(cursor=result)
            
    async def _cursor2dict(self, cursor: CursorResult) -> db_answer:
        ''' Converter of cursor to dictionary '''
        keys = cursor.keys()
        return [{key: row[key] for key in keys} for row in cursor]

    async def get_patterns(self) -> db_answer:
        ''' Get patterns list '''
        return await self._execute_query(query=SQLDB.query_get_patterns)


class NoSQLDB:
    ''' Class document db connectors '''

    @classmethod
    @debug_logger
    async def init(cls, params: init_params) -> int:
        ''' Async constructor for async creat_pool '''
        instance = NoSQLDB()
        
        conn_str = environ.get("connection_string", False)
        conn_str = conn_str if conn_str else params["connection_string"]
        logger.debug("NoSQLDB - init - conn_str=%s" % conn_str)

        final_str = 'redis://%s' % conn_str
        instance._pool = await aioredis.create_pool(
            final_str,
            minsize=params["minsize"],
            maxsize=params["maxsize"],
            encoding='utf-8'
        )
        return 0

    def __new__(cls, *args, **kwargs) -> Type["NoSQLDB"]:
        ''' Pattern singleton '''
        if not hasattr(cls, 'instance'):
            cls.instance = super(NoSQLDB, cls).__new__(cls)
        return cls.instance

    async def read(self, key: str) -> List[str]:
        '''  '''
        with await self._pool as conn:
            val = await conn.execute('lrange', key, 0, -1)
            return val

    async def write(self, key: str, msg: str) -> int:
        ''' Append message to list by key '''

        msg = "NoSQLDB - write - data: key=%s, msg=%s" % (key, msg)
        logger.debug(msg)

        with await self._pool as conn:
            await conn.execute('lpush', key, msg)

        return 0