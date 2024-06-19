import logging
import pandas as pd
from nwae.math.utils.Logging import Logging
from nwae.math.datasource.Credentials import Credentials
from nwae.math.datasource.DatastoreMaster import DatastoreMaster
from nwae.math.datasource.DatastoreInterface import DbParams

class TestHugeWriteRead:

    def __init__(
            self,
            csv_path,
            db_params,
            cols_keep = ('Faq Name', 'Utterance',),
            # minimum count of data in DB before we read back
            min_data = 11000,
            logger = None,
    ):
        self.csv_path = csv_path
        self.db_params = db_params
        self.cols_keep = cols_keep
        self.min_data = min_data
        self.logger = logger if logger is not None else logging.getLogger()

        self.df_csv = pd.read_csv(filepath_or_buffer=self.csv_path)
        self.df_csv = self.df_csv[list(self.cols_keep)]
        self.df_csv.dropna(inplace=True)
        self.logger.info(
            'Read from csv path "' + str(self.csv_path) + '" data shape ' + str(self.df_csv.shape)
            + ', final columns ' + str(self.df_csv.keys())
        )

        self.datastore = DatastoreMaster(
            db_params = self.db_params,
            logger = self.logger,
        ).get_data_store()
        self.db_index = 'TestHugeWriteRead'.lower()

        # Read data
        self.records = self.datastore.get_all(
            key = self.cols_keep[0],
            max_records = 1000000,
            tablename_or_index = self.db_index
        )
        self.logger.info('Existing data in index "' + str(self.db_index) + '" total records ' + str(len(self.records)))
        return

    def test(
            self,
    ):
        if len(self.records) < self.min_data:
            self.pump_in_data()
        return

    def pump_in_data(
            self,
    ):
        self.logger.info('Start pumping in data from csv...')
        for i, rec in enumerate(self.df_csv.to_dict('records')):
            self.logger.info('Adding record #' + str(i) + ': ' + str(rec))
            res = self.datastore.add(
                records = [rec],
                tablename_or_index = self.db_index,
            )
            self.logger.info('Result of add: ' + str(res))
            break

if __name__ == '__main__':
    c = Credentials(con_id='mark.local.os9208')
    TestHugeWriteRead(
        csv_path = 'faq_dataset.csv',
        db_params = DbParams(
            identifier = str(TestHugeWriteRead),
            db_type = c.DB_TYPE,
            db_host = c.DB_HOST,
            db_port = c.DB_PORT,
            db_scheme = c.DB_SCHEME,
            db_username = c.DB_USERNAME,
            db_password = c.DB_PASSWD,
            db_verify_certs = False,
        ),
        logger = Logging.get_default_logger(log_level=logging.INFO, propagate=False)
    ).test()
    exit(0)
