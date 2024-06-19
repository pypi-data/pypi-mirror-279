import logging
import os
import threading
import json
import numpy as np
from datetime import datetime
from fitxf.math.datasource.vecdb.metadata.MetadataInterface import MetadataInterface
from fitxf.math.datasource.DatastoreInterface import DbParams
from fitxf.math.datasource.DatastoreMaster import DatastoreMaster
from fitxf.math.utils.Logging import Logging
from fitxf.math.utils.Env import Env
from fitxf.math.utils.EnvironRepo import EnvRepo


class ModelMetadata(MetadataInterface):

    DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'

    # For stupid DBs like Opensearch/Elasticsearch, be careful when changing column names,
    # they might cause add/delete to behave differently
    COL_METADATA_INDEX = 'metadata_index'           # Index that this metadata refers to
    COL_METADATA_IDENTIFIER = 'metadata_identifier' # What kind of metadata (e.g. model, embedding size)
    # any integer counter
    COL_METADATA_TIMESTAMP = 'metadata_timestamp'
    COL_METADATA_VALUE = 'content'

    def __init__(
            self,
            # name to identify which user/table/etc this metadata is referring to
            user_id,
            metadata_tbl_name = 'model_metadata',
            logger = None,
    ):
        super().__init__(
            user_id = user_id,
            metadata_tbl_name = metadata_tbl_name,
            logger = logger,
        )

        self.db_params_metadata = DbParams.get_db_params_from_envvars(
            identifier = str(self.__class__),
            # fill in later below
            db_create_tbl_sql = None,
            db_table_or_index = self.metadata_tbl_name,
            verify_certs = os.environ.get("VERIFY_CERTS", "1").lower() in ['1', 'true', 'yes'],
        )

        # For metadata
        # Change create table syntax
        if self.db_params_metadata.db_type in ('mysql',):
            self.db_params_metadata.db_create_table_sql = \
                "CREATE TABLE `<TABLENAME>` " \
                + "(`" \
                + str(self.COL_METADATA_INDEX) + "` varchar(255) NOT NULL" \
                + ", `" + str(self.COL_METADATA_IDENTIFIER) + "` varchar(255) NOT NULL" \
                + ", `" + str(self.COL_METADATA_TIMESTAMP) + "` double DEFAULT NULL" \
                + ", `" + str(self.COL_METADATA_VALUE) + "` varchar(5000) DEFAULT NULL" \
                + ")"
        # + ', PRIMARY KEY (' + str(self.COL_METADATA_INDEX) + ', ' + str(self.COL_METADATA_IDENTIFIER) + ')' \
        self.logger.info(
            'Using DB create table sql syntax as "' + str(self.db_params_metadata.db_create_table_sql)
            + '" for DB type "' + str(self.db_params_metadata.db_type) + '"'
        )

        # Model params, last update times, etc.
        self.db_metadata = DatastoreMaster(
            db_params = self.db_params_metadata,
            logger = self.logger,
        ).get_data_store()
        self.logger.info('Connected to underlying metadata DB ' + str(self.db_params_metadata.get_db_info()))

        self.__mutex_db = threading.Lock()
        self.last_cleanup_time = datetime(year=2000, month=1, day=1)
        self.min_interval_secs_cleanup = 30
        return

    def __get_specific_metadata(
            self,
            metadata_identifier,
    ):
        try:
            self.__mutex_db.acquire()

            match_phrase = {
                self.COL_METADATA_INDEX: self.user_id,
                self.COL_METADATA_IDENTIFIER: metadata_identifier,
            }
            rows = self.db_metadata.get(
                match_phrase = match_phrase,
                tablename_or_index = self.db_params_metadata.db_table_or_index,
            )
            if len(rows) == 0:
                raise Exception('No metadata returned for ' + str(match_phrase) + '. Returned rows ' + str(rows))
            elif len(rows) == 1:
                return rows[0]
            else:
                last_timestamp = -np.inf
                row_keep = None
                for r in rows:
                    timestamp = r[self.COL_METADATA_TIMESTAMP]
                    if timestamp > last_timestamp:
                        row_keep = r

                self.logger.debug(
                    'Metadata returned > 1 rows from table/index "' + str(self.db_params_metadata.db_table_or_index)
                    + '": ' + str(rows) + ', keep: ' + str(row_keep)
                )
                return row_keep
        except Exception as ex:
            self.logger.error(
                'Error getting metadata "' + str(metadata_identifier) + '", returning "' + str(None) + '": ' + str(ex)
            )
        finally:
            self.__mutex_db.release()

    def get_metadata_db_data_last_update(
            self,
    ):
        try:
            row = self.__get_specific_metadata(
                metadata_identifier = 'lastUpdateTime',
            )
            return datetime.strptime(row[self.COL_METADATA_VALUE], self.DATETIME_FORMAT)
        except Exception:
            return None

    def get_metadata_model_last_update(
            self,
    ):
        try:
            row = self.__get_specific_metadata(
                metadata_identifier = 'model',
            )
            return row[self.COL_METADATA_VALUE]
        except Exception:
            return None

    # signify that model has been updated
    def update_metadata_model_updated(
            self,
            llm_path: str,
            model_save_json_string: str,
    ):
        insert_records = [
            {
                self.COL_METADATA_INDEX: self.user_id,
                self.COL_METADATA_IDENTIFIER: 'model',
                self.COL_METADATA_VALUE: json.dumps({
                        'llm_path': llm_path,
                        'model_save_json_string': model_save_json_string,
                    },
                    ensure_ascii = False,
                )
            }
        ]
        return self.__update_metadata_to_db(
            tablename = self.db_params_metadata.db_table_or_index,
            records = insert_records,
        )

    def update_metadata_db_raw_data_updated(self):
        tnow = datetime.now()
        last_update_record = [
            {
                self.COL_METADATA_INDEX: self.user_id,
                self.COL_METADATA_IDENTIFIER: 'lastUpdateTime',
                self.COL_METADATA_VALUE: tnow.strftime(self.DATETIME_FORMAT),
            }
        ]

        # Add lastUpdateTime key to insert records
        return self.__update_metadata_to_db(
            tablename = self.db_params_metadata.db_table_or_index,
            records = last_update_record,
        )

    def __update_metadata_to_db(
            self,
            tablename,
            records,
    ):
        # add timestamp to records
        tdif = datetime.now() - datetime(year=2023, month=12, day=11)
        timestamp = tdif.days + tdif.seconds/(86400) + tdif.microseconds/(86400*1000000)
        for r in records:
            r[self.COL_METADATA_TIMESTAMP] = timestamp

        try:
            self.__mutex_db.acquire()
            tdif_cleanup = datetime.now() - self.last_cleanup_time
            tdif_cleanup_secs = tdif_cleanup.days * 86400 + tdif_cleanup.seconds + tdif_cleanup.microseconds / 1000000
            if tdif_cleanup_secs > self.min_interval_secs_cleanup:
                for mp in [
                    {
                        self.COL_METADATA_INDEX: d[self.COL_METADATA_INDEX],
                        self.COL_METADATA_IDENTIFIER: d[self.COL_METADATA_IDENTIFIER]
                    } for d in records
                ]:
                    try:
                        # Table might not exist if first time
                        res = self.db_metadata.delete(
                            tablename_or_index = tablename,
                            match_phrase = mp,
                        )
                        self.logger.info(
                            'Deleted from metadata table using match phrase ' + str(mp) + ', result ' + str(res)
                        )
                    except Exception as ex:
                        # For
                        self.logger.error('Error deleting metadata with match phrase "' + str(mp) + '": ' + str(ex))
                    # update last cleanup time
                    self.last_cleanup_time = datetime.now()
            else:
                self.logger.info('Ignore metadata cleanup, last done only ' + str(tdif_cleanup_secs) + ' ago')

            self.db_metadata.add(
                tablename_or_index = tablename,
                records = records,
            )
            self.logger.info(
                'Successfully wrote metadata records to "' + str(tablename) + '": '
                + str([{k: str(v)[0:min(300,len(str(v)))] for k, v in r.items()} for r in records])
            )
            return records
        finally:
            self.__mutex_db.release()

    def cleanup(
            self,
    ):
        try:
            self.__mutex_db.acquire()
            res = self.db_metadata.delete(
                match_phrase = {self.COL_METADATA_INDEX: self.user_id},
                tablename_or_index = self.db_params_metadata.db_table_or_index,
            )
            self.logger.info('Successfully deleted metadata for index "' + str(self.user_id) + '": ' + str(res))
            return {'deleted': res['deleted']}
        except Exception as ex:
            self.logger.info('Error delete metadata for index "' + str(self.user_id) + '": ' + str(ex))
        finally:
            self.__mutex_db.release()


if __name__ == '__main__':
    er = EnvRepo(repo_dir=os.environ.get("REPO_DIR", None))
    Env.set_env_vars_from_file(env_filepath=er.REPO_DIR + '/.env.fitx.fmath.ut')
    ModelMetadata(
        user_id = 'test',
        logger = Logging.get_default_logger(log_level=logging.INFO, propagate=False)
    )
    exit(0)
