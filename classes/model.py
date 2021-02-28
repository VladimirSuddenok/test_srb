from classes.backed_connectors import SQLDB, NoSQLDB
from typing import Tuple 
from asyncio import sleep
from classes.parents_classes.base_class import BaseClass
from re import compile

# vars
sqldb = SQLDB()
nosqldb = NoSQLDB()

class Patterns(BaseClass):
    ''' Model of pattern 
        Implements methods for processing pattern
    '''

    parameters = ["update_delay"]
    _instances  = {}
    _ids = []
    
    def __init__(self, rule_name: str, pattern: str):
        ''' Constructor '''
        self._rule_name = rule_name
        self._pattern   = compile(pattern)

    @property
    def rule_name(self) -> str:
        ''' Property for getting of rule name '''
        return self._rule_name

    @classmethod
    async def check_message(cls, msg: str) -> Tuple[bool, str]:
        ''' Processing of message '''
        status, message = False, "there are no matches"
        
        # do check for each model 
        for id in Patterns._ids:
            instance = cls._instances[id]
            result = instance.check_by_patter(msg=msg)

            if result:
                status = True
                message = instance.rule_name
                break

            else:
                continue
        
        # write msg to document
        if status:
            await nosqldb.write(key=message, msg=msg)
        
        return status, message

    async def _check_by_patter(self, msg) -> bool:
        ''' Search matches in message '''
        data = self._pattern.findall(msg)
        return True if len(data) > 0 else False
        
    @classmethod
    async def load_patterns(cls) -> int:
        ''' Coroutine for load new patterns 
            Loading once every <update_delay> seconds
        '''
        while True:
            # load all patterns
            dict_patterns = await sqldb.get_patterns()
            for record in dict_patterns:
                p_id = record.pop('id')
                # if there is no patterns
                if not cls._instances.get(p_id, False):
                    cls._instances[p_id] = Patterns(**record)

                cls._ids = list(cls._instances.keys())
                
            await sleep(cls.update_delay)

        return 0