import logging
import builtins
import os
from nwae.math.datasource.DatastoreInterface import DatastoreInterface, DbParams, DatastoreInterfaceUnitTest
import threading
from nwae.math.utils.Logging import Logging
from nwae.math.utils.Env import Env
from nwae.math.utils.EnvironRepo import EnvRepo

#
# To be used for mid-sized memory caches.
# We don't use pandas to minimize weird behaviors with text data if using DataFrames
# and also to keep things as simple as possible with simple lists and dictionaries.
#
class MemoryCache(DatastoreInterface):

    PARAM_RETURN_TYPE = 'return_type'

    RETURN_TYPE_COPY = 'copy'
    RETURN_TYPE_REF = 'reference'
    RETURN_TYPE_INDEX = 'index'
    ALLOWED_RETURN_TYPES = (RETURN_TYPE_COPY, RETURN_TYPE_REF, RETURN_TYPE_INDEX,)

    def __init__(
            self,
            db_params: DbParams,
            ignore_warnings = False,
            logger = None,
    ):
        super().__init__(
            db_params = db_params,
            logger = logger,
            ignore_warnings = ignore_warnings,
        )
        # This mutex will only work by thread/worker, for multithread/worker use file locks or RabbitMq
        self.__mutex = threading.Lock()

        # List of dictionary records
        self.records = []
        return

    def connect(
            self,
    ):
        return

    def get(
            self,
            # e.g. {"answer": "take_seat"}
            match_phrase,
            match_condition = 'AND',
            tablename = None,
            request_timeout = 20.0,
    ):
        assert type(match_phrase) is dict
        data = []
        for idx, rec in enumerate(self.records):
            is_match = True if match_condition == 'AND' else False
            for k in match_phrase.keys():
                part_condition = (rec[k] == match_phrase[k])
                if match_condition == 'AND':
                    is_match = is_match and part_condition
                else:
                    is_match = is_match or part_condition
                    self.logger.info(str(is_match) + ', ' + str(rec[k]) + ', ' + str(match_phrase[k]))
            if is_match:
                self.logger.info(
                    'Match = ' + str(is_match) + ' Match phrase ' + str(match_phrase) + ' record ' + str(rec))
                rec_safe_copy = {k: v for k, v in rec.items()}
                assert builtins.id(rec) != builtins.id(rec_safe_copy)
                data.append(rec_safe_copy)
        return data

    def get_all(
            self,
            key = None,
            max_records = 10000,
            tablename = None,
            request_timeout = 20.0,
    ):
        safe_copy = []
        for idx, rec in enumerate(self.records):
            safe_rec = {k: v for k, v in rec.items()}
            safe_copy.append(safe_rec)
        return safe_copy

    def get_indexes(self):
        return 'This function not supported'

    def delete_index(
            self,
            tablename,
    ):
        return 'This function not supported'

    def add(
            self,
            # list of dicts
            records,
            tablename = None,
    ):
        assert type(records) in (list, tuple,)
        try:
            self.__mutex.acquire()
            for rec in records:
                self.records.append(rec)
        except Exception as ex:
            self.logger.error('Error occurred: ' + str(ex))
        finally:
            self.__mutex.release()

    def delete(
            self,
            match_phrase,
            match_condition = 'AND',
            tablename = None,
    ):
        try:
            self.__mutex.acquire()
            recs_to_be_deleted = self.get(
                match_phrase = match_phrase,
                match_condition = match_condition,
                tablename = tablename,
            )
            self.logger.info(
                'To be deleted for match phrase ' + str(match_phrase) + '\n' + str(recs_to_be_deleted)
            )
            total_deleted = 0
            for rec in recs_to_be_deleted:
                self.records.remove(rec)
                total_deleted += 1
            return {'deleted': total_deleted}
        except Exception as ex:
            return {'error': str(ex)}
        finally:
            self.__mutex.release()


if __name__ == '__main__':
    Env.set_env_vars_from_file(env_filepath=EnvRepo().REPO_DIR + os.sep + '.env.nwae.math.ut')
    DatastoreInterfaceUnitTest(
        ChildClass = MemoryCache,
        logger = Logging.get_default_logger(log_level=logging.INFO, propagate=False)
    ).test(
        tablename = 'memorycachetest',
    )
    exit(0)
