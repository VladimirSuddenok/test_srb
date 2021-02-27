import sqlite3
import redis
from sqlalchemy import text, pool
from sqlalchemy.ext.asyncio import create_async_engine

class SQLDB:

    def __init__(
            self,
            meth="get",
            params={}
        ):
        ''' 
            :meth: str - init/get
        '''
        if meth == "init":
            self._pool = create_async_engine(
                params["connection_string"],
                poolclass=pool.QueuePool,
                pool_size=params["pool_size"],
                max_overflow=params["max_overflow"]
            )

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(SQLDB, cls).__new__(cls)
        return cls.instance
    
    async def execute_query(self, query):
        '''  '''
        async with self._pool.begin() as conn:
            result = await conn.execute(text(query))
            return await self._cursor2dict(cursor=result)
            
    async def _cursor2dict(self, cursor):
        '''  '''
        keys = cursor.keys()
        return [{key: row[key] for key in keys} for row in cursor]

class NoSQLDB:
    pass