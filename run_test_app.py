''' Endpoint '''

import asyncio
#from settings import Setup
from classes.server import Server
from classes.backed_connectors import SQLDB, NoSQLDB

version = "0.002.001"

async def test_run_server():
    settings = {"host": "127.0.0.1", "port": 8080}
    Server.set_cls_params(**settings)
    server_runner = Server.get_runner()
    print("server_run_cor", server_runner)
    await server_runner

    return 0

async def test_sql_connection():
    settings = {
        "connection_string": r"sqlite:///C:\\Users\\Владимир\\Desktop\\сбер\\foo.db",
        "pool_size": 3,
        "max_overflow": 0
    }
    #SQLBD.set_cls_params(**settings)
    sql = SQLDB(params=settings)
    show_table = '''
    SELECT 
        name
    FROM 
        sqlite_master 
    WHERE 
        type ='table' AND 
        name NOT LIKE 'sqlite_%';
    '''
    test_query = '''
        select * from test_second;
    '''

    print(await sql.execute_query(query=test_query))
    #print ("sql", sql)
    #print("sql", sql.__dict__)
    #sql = SQLBD()
    #print ("sql", sql)
    ##Server.set_cls_params(**settings)
    ##server_runner = Server.get_runner()
    #print("sql", sql.__dict__)
    #await server_runner

    return 0

async def test_no_sql_connection():
    settings = {"connetion_string": "127.0.0.1:6379", "minsize": 1, "maxsize": 3}
    await NoSQLDB.init(params=settings)
    nosql = NoSQLDB()
    print(nosql.__dict__)
    print(nosql)
    await nosql.write()
    res = await nosql.read()
    print("res", res)
    #Server.set_cls_params(**settings)
    #server_runner = Server.get_runner()
    #print("server_run_cor", server_runner)
    #await server_runner

    return 0

async def main():
    # settings up classes
    #s = Setup()
    # build server instances
    #server = Server()
    #start_func, args = server.get_runner()
    
    await asyncio.gather(
        test_no_sql_connection()
        # print start log
        # run server
    )

if __name__ == "__main__":
    asyncio.run(main())