"""Logger for OUTLIERS app"""

class Logger:
    '''Logger class for OUTLIERS app. Support for debug and error message handling'''
    __DEBUGLVL = 0

    def __init__(self, mongo):
        self.mongo = mongo
        log_collection = mongo.db.logger
        debug_data = log_collection.find_one({'_id': 'global_debug_level'})
        Logger.__DEBUGLVL = debug_data['debug_level']

    def debug(self, debuglvl, function_name, debug_message, **kwargs):
        if self.__DEBUGLVL >= debuglvl:
            print(f'DEBUG   {function_name}   {debug_message}')

        if self.__DEBUGLVL >= 5 and kwargs:
            print(f'DEBUG   DUMP:')
            
            for key, value in kwargs.items():
                if 'password' == key:
                    continue
                print(f'DEBUG          {key} : {value}')

    def error(self, debuglvl, function_name, error_message, **kwargs):
        if self.__DEBUGLVL >= debuglvl:
            print(f'ERROR   {function_name}   {error_message}')

        if self.__DEBUGLVL >= 5 and kwargs:
            print(f'ERROR   DUMP:')
        
            for key, value in kwargs.items():
                if 'password' == key:
                    continue
                print(f'ERROR          {key} : {value}')
    
    def scheduler(self, scheduler_obj):
        scheduler_obj.print_jobs()
    
    def set_debug_lvl(self, debug_lvl):
        Logger.__DEBUGLVL = int(debug_lvl)
        log_collection = self.mongo.db.logger
        try:
            log_collection.update_one({'_id' : 'global_debug_level'}, {'$set' : {'debug_level': int(debug_lvl)}}, upsert = False)
        except Exception as e:
            self.error(0, 'Logger.set_debug_lvl', f'[{e}]')
    
    def get_debug_lvl(self):
        return Logger.__DEBUGLVL