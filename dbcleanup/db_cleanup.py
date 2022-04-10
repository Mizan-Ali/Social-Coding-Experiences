import dbcleanup.constants as constants
from hashlib import md5
from logger import Logger

logger = Logger()

class DBCleanup:

    def __init__(self, key):
        self.secret_key = key


    def validate_key(self):
        function = 'validate_key'
        logger.debug(function, "Validating DB deleteion key")
        if md5(self.secret_key.encode()).digest() != constants.DB_DELETION_SECRET_KEY_HASH:
            logger.error(function, "Wrong DB deletion key provided. Cannot delete DB.")
            self.curr_locale = ''
            return False
        
        logger.debug(function, "DB deletion key validated successfully")
        return True


    def initiate_db_cleanup(self, mongo):
        function = 'initiate_db_cleanup'
        logger.debug(function, "Initiating complete DB cleanup")
        logger.debug(function, "Executing delete operation")
        ret = {}
        try:
            logger.debug(function, "Attempting to delete users collection")
            users_collection = mongo.db.users
            ret = users_collection.delete_many({})
            logger.debug(function, "Users collection deleted", **{'DeletedCount': ret.deleted_count, 'IsAcknowledged': ret.acknowledged})


            logger.debug(function, "Attempting to delete github collection")
            github_collection = mongo.db.github
            ret = github_collection.delete_many({})
            logger.debug(function, "Github collection deleted", **{'DeletedCount': ret.deleted_count, 'IsAcknowledged': ret.acknowledged})

            logger.debug(function, "Attempting to delete codechef collection")
            codechef_collection = mongo.db.codechef
            ret = codechef_collection.delete_many({})
            logger.debug(function, "Codechef collection deleted", **{'DeletedCount': ret.deleted_count, 'IsAcknowledged': ret.acknowledged})

            logger.debug(function, "Attempting to delete codeforces collection")
            codeforces_collection = mongo.db.codeforces
            ret = codeforces_collection.delete_many({})
            logger.debug(function, "Codeforces collection deleted", **{'DeletedCount': ret.deleted_count, 'IsAcknowledged': ret.acknowledged})

            logger.debug(function, "Attempting to delete votes collection")
            votes_collection = mongo.db.votes
            ret = votes_collection.delete_many({})
            logger.debug(function, "Votes collection deleted", **{'DeletedCount': ret.deleted_count, 'IsAcknowledged': ret.acknowledged})

        except Exception as e:
            errStr = f'Table failed to delete with error : [{e}]'
            logger.error(function, errStr, **{'DeletedCount': ret.deleted_count, 'IsAcknowledged': ret.acknowledged})
            return {'cleanup_status' : constants.CLEANUP_OP_FAILURE} 
        
        return {'cleanup_status' : constants.CLEANUP_OP_SUCCESS} 
