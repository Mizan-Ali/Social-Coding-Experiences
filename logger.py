"""Logger for OUTLIERS app"""

class Logger:
    '''Logger class for OUTLIERS app. Support for debug and error message handling'''
    
    def debug(function_name, debug_message, user_name = "user not found", **kwargs):
        print(f'DEBUG   {function_name}   {debug_message}')

        if kwargs:
            print(f'DEBUG   DUMP:')
        
        for key, value in kwargs:
            print(f'               {key} : {value}')

    def error(function_name, error_message, user_name = "", **kwargs):
        print(f'ERROR   {function_name}   {error_message}')

        if kwargs:
            print(f'ERROR   DUMP:')
        
        for key, value in kwargs:
            print(f'               {key} : {value}')
    
    def scheduler(scheduler_obj):
        scheduler_obj.print_jobs()