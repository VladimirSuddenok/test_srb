from sqlalchemy import text, pool
from sqlalchemy.ext.asyncio import create_async_engine
import aioredis

class SQLDB:
    ''' Class relation db connectors '''
    def __init__(self, params={}):
        '''  '''
        if params:
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
    ''' Class document db connectors '''

    @classmethod
    async def init(cls, params):
        ''' async init for creating pool '''
        instance = NoSQLDB()
        final_str = 'redis://%s' % params["connetion_string"]
        instance._pool = await aioredis.create_pool(
            final_str,
            minsize=params["minsize"], 
            maxsize=params["maxsize"]
        )
        print("instance", instance)
        return 0

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(NoSQLDB, cls).__new__(cls)
        return cls.instance

    async def read(self, data=False):
        '''  '''
        with await self._pool as conn:
            val = await conn.execute('get', 'my-key')
            return val
            

    async def write(self, data=False):
        '''  '''
        with await self._pool as conn:
            await conn.execute('set', 'my-key', 'value')

        return 0
    #    with await pool as conn:    # low-level redis connection
    #    await conn.execute('set', 'my-key', 'value')
    #    val = await conn.execute('get', 'my-key')
    #print('raw value:', val)
    #pool.close()
    #await pool.wait_closed()    # closing all open connections