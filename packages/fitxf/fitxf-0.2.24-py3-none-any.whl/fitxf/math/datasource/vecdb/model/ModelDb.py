import os
import re
import time
import numpy as np
from fitxf.math.algo.encoding.Base64 import Base64
from fitxf.math.datasource.vecdb.model.ModelDbInterface import ModelDbInterface
from fitxf.math.datasource.DatastoreInterface import DbParams, DatastoreInterface
from fitxf.math.datasource.DatastoreMaster import DatastoreMaster


class ModelDb(ModelDbInterface):

    CREATE_TABLE_CMD_TEMPLATE = {
        'memory': None,
        'csv': None,
        'mysql': """CREATE TABLE `<TABLENAME>` (
                        `<CONTENT>` TEXT NOT NULL,
                        `<LABEL_USER>` varchar(255) NOT NULL,
                        `<LABEL_NUMBER>` int NOT NULL,
                        `<ENCODING_B64>` TEXT NOT NULL
                    )""",
    }

    def __init__(
            self,
            tablename: str,
            col_content: str,
            col_label_user: str,
            col_label_standardized: str,
            col_embedding: str,
            max_records: int,
            logger = None,
    ):
        super().__init__(
            tablename = tablename,
            col_content = col_content,
            col_label_user = col_label_user,
            col_label_standardized = col_label_standardized,
            col_embedding = col_embedding,
            max_records = max_records,
            logger = logger,
        )
        self.base64_encoder = Base64(logger=self.logger)
        self.connect_to_underlying_db()
        return

    def get_create_table_db_cmd(
            self,
            db_type,
    ) -> str:
        template = self.CREATE_TABLE_CMD_TEMPLATE[db_type]
        if template is None:
            return None
        for placeholder, value in [
            ('<CONTENT>', self.col_content),
            ('<LABEL_USER>', self.col_label_user),
            ('<LABEL_NUMBER>', self.col_label_standardized),
            ('<ENCODING_B64>', self.col_embedding),
        ]:
            template = re.sub(pattern=placeholder, repl=value, string=template)
        self.logger.info('Create table DB cmd for type "' + str(db_type) + '": ' + str(template))
        return template

    def get_db_params(self) -> DbParams:
        return self.db_params

    def get_underlying_db(self) -> DatastoreInterface:
        return self.underlying_db

    def connect_to_underlying_db(
            self,
    ):
        self.underlying_db = DatastoreMaster(
            db_params = self.db_params,
            logger = self.logger,
        ).get_data_store()
        self.logger.info('Connected to underlying DB ' + str(self.db_params.get_db_info()))
        return

    def load_model_from_underlying_db_with_max_retries(
            self,
            max_tries = 1,
    ):
        try_count = 0
        while True:
            try_count += 1
            try:
                records_from_db = self.__load_model_from_underlying_db_job()
                self.logger.info(
                    'Done load from underlying DB, loaded data len ' + str(len(records_from_db))
                    + ', try no. ' + str(try_count) + '.'
                )
                # if try_count < 3:
                #     raise Exception('Fake fail count ' + str(try_count))
                return records_from_db
            except Exception as ex:
                self.logger.error('Loading from underlying DB failed ' + str(try_count) + ' times: ' + str(ex))
                if try_count >= max_tries:
                    raise Exception('Loading from primary DB max tries reached ' + str(max_tries))
                # Sleep for some random time 2-5secs
                time.sleep(2+3*np.random.rand())

    #
    # This critical function keeps our model updated with whatever in DB/memory cache
    #
    def __load_model_from_underlying_db_job(
            self,
    ):
        try:
            # Get all encoded texts, standardized labels, text encoding from memory cache
            all_records = self.underlying_db.get_all(
                key = self.col_content,
                tablename_or_index = self.tablename,
                max_records = self.max_records,
                request_timeout = int(os.environ.get('DATA_LOAD_REQUEST_TIMEOUT', 30)),
                return_db_style_records = True,
            )
            self.logger.info('Retrieved all records total length ' + str(len(all_records)))
            # if not all_records:
            #     raise Exception(
            #         'No data retrieved from data cache "' + str(self.db_params.db_info) + '"'
            #     )

            # Embedding column will be removed below
            return all_records
        except Exception as ex:
            errmsg = 'Error loading model from underlying DB' + str(self.db_params.get_db_info()) \
                     + ' Exception message: ' + str(ex)
            self.logger.error(errmsg)
            raise Exception(errmsg)


    def convert_csv_string_array_to_float_array(
            self,
            string_array,
            custom_chars_remove,
    ):
        return self.underlying_db.convert_csv_string_array_to_float_array(
            string_array = string_array,
            custom_chars_remove = custom_chars_remove,
        )


if __name__ == '__main__':
    exit(0)
