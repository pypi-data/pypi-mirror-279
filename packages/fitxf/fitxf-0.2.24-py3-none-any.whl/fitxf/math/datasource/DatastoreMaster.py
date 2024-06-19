import logging
import re
import os
from fitxf.math.datasource.DatastoreInterface import DbParams
from fitxf.math.datasource.Csv import Csv
from fitxf.math.datasource.MemoryCache import MemoryCache
from fitxf.math.datasource.MySql import MySql
from fitxf.math.datasource.OpenSearch import OpenSearchDS
from fitxf.math.datasource.ElasticSearch import ES
from fitxf.math.utils.Env import Env
from fitxf.math.utils.Logging import Logging


class DatastoreMaster:

    def __init__(
            self,
            db_params: DbParams,
            logger = None,
    ):
        self.db_params = db_params
        assert type(self.db_params) is DbParams, 'Wrong type for db_params "' + str(type(self.db_params)) + '"'
        self.logger = logger if logger is not None else logging.getLogger()
        return

    def get_data_store(
            self,
    ):
        if self.db_params.db_type == 'csv':
            assert not re.match(pattern="/", string=self.db_params.db_table), \
                'Must not contain full path in table name or index "' + str(self.db_params.db_table) + '"'
            filepath = self.db_params.db_root_folder + '/' + self.db_params.db_table
            return Csv(
                db_params = self.db_params,
                logger = self.logger,
            )
        elif self.db_params.db_type in ('mysql',):
            self.logger.info(
                'Trying to initialize class "' + str(MySql) + '",  params ' + str(self.db_params.get_db_info())
            )
            db = MySql(
                host = self.db_params.db_host,
                port = self.db_params.db_port,
                username = self.db_params.db_username,
                password = self.db_params.db_password,
                database = self.db_params.db_database,
                logger = self.logger,
            )
            db.connect(
                other_params = {'create_table_sql': self.db_params.db_create_table_sql},
            )
            return db
        elif self.db_params.db_type in ('elasticsearch', 'opensearch',):
            ignore_warnings = self.db_params.params_other.get('ignore_warnings', True)
            messed_by_haystack = self.db_params.params_other.get('messed_by_haystack', False)
            DbClass = ES if self.db_params.db_type == 'elasticsearch' else OpenSearchDS
            self.logger.info(
                'Trying to initialize class "' + str(DbClass) + '", ignore warnings "' + str(ignore_warnings)
                + '", messed by haystack "' + str(messed_by_haystack) + '", and params ' + str(self.db_params.get_db_info())
            )
            db = DbClass(
                host     = self.db_params.db_host,
                port     = self.db_params.db_port,
                username = self.db_params.db_username,
                password = self.db_params.db_password,
                database = self.db_params.db_database,
                ignore_warnings = ignore_warnings,
                messed_by_haystack = messed_by_haystack,
                logger   = self.logger,
            )
            db.connect(verify_certs=self.db_params.db_verify_certs)
            return db
        elif self.db_params.db_type == 'memory':
            # Data kept as dict records in memory, no physical files or DB
            # Means only exist during program execution
            return MemoryCache(
                db_params = None,
                logger = self.logger,
            )
        else:
            raise Exception('Not supported data store type "' + str(self.db_params.db_type) + '"')


if __name__ == '__main__':
    Env.set_env_vars_from_file(env_filepath=os.environ["REPO_DIR"] + '/.env.fitxf.math')
    dbp = DbParams(
        identifier = 'test set',
        db_type   = os.environ["DB_TYPE"],
        db_host   = os.environ["DB_HOST"],
        db_port   = os.environ["DB_PORT"],
        db_scheme = os.environ["DB_SCHEME"],
        db_username = os.environ["DB_USERNAME"],
        db_password = os.environ["DB_PASSWORD"],
        db_verify_certs = os.environ["VERIFY_CERTS"],
        params_other ={'ignore_warnings': True},
        logger = Logging.get_default_logger(log_level=logging.INFO, propagate=False),
    )
    db = DatastoreMaster(db_params=dbp)
    db.get_data_store()
    exit(0)
