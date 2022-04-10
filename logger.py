"""Logger for OUTLIERS app"""


class Logger:
    '''Logger class for OUTLIERS app. Support for debug and error message handling'''
    
    def debug(self, function_name, debug_message, **kwargs):
        print(f'DEBUG   {function_name}   {debug_message}')

        if kwargs:
            print(f'DEBUG   DUMP:')
            
            for key, value in kwargs.items():
                if 'password' == key:
                    continue
                print(f'               {key} : {value}')

    def error(self, function_name, error_message, **kwargs):
        print(f'ERROR   {function_name}   {error_message}')


        if kwargs:
            print(f'ERROR   DUMP:')
        
            for key, value in kwargs.items():
                if 'password' == key:
                    continue
                print(f'               {key} : {value}')
    
    def scheduler(self, scheduler_obj):
        scheduler_obj.print_jobs()