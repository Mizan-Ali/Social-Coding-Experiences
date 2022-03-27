import platform
import os
import dbcleanup.constants as constants
from hashlib import md5

class DBCleanup:

    def __init__(self, key):
        self.cwd = os.path.abspath(os.curdir)
        self.curr_locale = platform.system()
        self.cleanup_command = ''
        self.secret_key = key


    def validate_key(self):
        if md5(self.secret_key.encode()).digest() != constants.DB_DELETION_SECRET_KEY_HASH:
            self.curr_locale = ''
            return False

        return True


    def initiate_db_cleanup(self):
        path_to_rem = self.cwd
        print(path_to_rem)
        if constants.OSTYPE_WINDOWS == self.curr_locale:
            path_to_rem += constants.DB_FILEPATH_WINDOWS
        else:
            path_to_rem += constants.DB_FILEPATH_UNIX

        try:
            os.remove(path_to_rem)
        except Exception as e:
            print(f'\n\n{e}\n\n')
            return {'cleanup_status' : constants.CLEANUP_OP_FAILURE} 
            
        ret = self.check_db_cleanup_status()

        if ret:
            return {'cleanup_status' : constants.CLEANUP_OP_FAILURE}
        
        return {'cleanup_status' : constants.CLEANUP_OP_SUCCESS} 

    def check_db_cleanup_status(self):

        if self.curr_locale == constants.OSTYPE_WINDOWS:
            return os.path.exists(constants.DB_FILEPATH_WINDOWS)

        return os.path.exists(constants.DB_FILEPATH_UNIX)

