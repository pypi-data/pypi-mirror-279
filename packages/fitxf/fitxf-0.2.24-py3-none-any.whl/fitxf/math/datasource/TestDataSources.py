import logging
import os.path
import unittest
import builtins
import pandas as pd
from io import StringIO
from nwae.math.datasource.ElasticSearch import ES
from nwae.math.datasource.Csv import Csv
from nwae.math.datasource.MemoryCache import MemoryCache


class TestDataSources(unittest.TestCase):

    def test_csv(self):
        DATAPATH = 'data_test.csv'

        ds = Csv(filepath=DATAPATH)
        ds.connect()
        rows = ds.get_all(key='')
        [ds.delete(match_phrase={'id': r['id']}) for r in rows]

        new_records = [
            {'id': 100, 'text': "give me today shows", 'answer': ' today_showing', 'val': 9.8},
            {'id': 101, 'text': "davai menya kino sigodnya", 'answer': ' today_showing', 'val': 1.2},
            {'id': 102, 'text': "remain text", 'answer': 'random'},
            {'id': 103, 'text': "missing column answer"},
        ]
        ds.add(records=new_records)
        rows = ds.get_all(key='')
        self.assertTrue(
            expr = len(rows) == len(new_records),
            msg = 'Length of retrieved ' + str(len(rows)) + ' not same with data added ' + str(len(new_records))
        )
        len_prev = len(rows)

        new_records = [
            {'id': 104, 'text': "missing column answer 2", 'no_such_column': 'asdf'},
        ]
        ds.add(records=new_records)
        rows = ds.get_all(key='')
        self.assertTrue(
            expr = len(rows) == len(new_records) + len_prev,
            msg = 'Length of retrieved ' + str(len(rows)) + ' not same with data added ' + str(len(new_records))
        )

        for id in [101]:
            ds.delete(match_phrase={'id': id})
            print('After DELETE ' + str(id) + '..')
            rows = ds.get_all(key='')
            [print(r) for r in rows]

        print('Final records')
        [print(r) for r in ds.get_all(key='')]


    def test_es(self):
        ES_HOST = 'localhost'
        ES_PORT = 9777
        ES_USERNAME = 'elastic'
        ES_PASSWORD = 'CDMolGy7ex5zNgF6JmfQ'
        ES_SCHEME = 'https'
        ES_INDEX = 'xtest'

        obj = ES(
            ignore_warnings = True,
        )
        obj.connect(
            host = ES_HOST,
            port = ES_PORT,
            username = ES_USERNAME,
            password = ES_PASSWORD,
            scheme   = ES_SCHEME,
            verify_certs = False,
        )

        print(obj.get_indexes())
        # for idx in ['en_faq', 'en_qa']:
        #     print(obj.delete_index(tablename_or_index=idx))

        csvpath = r'./es_data.csv'
        mode = ''
        if mode == 'new':
            # For Haystack/ElasticSearch, permitted=('text', 'table', 'image', 'audio')
            # Haystack version 1.14.0 cannot even read Elastic Search if there is no "content_type" column
            obj.delete_all(key='answer', tablename_or_index=ES_INDEX)
            if os.path.exists(csvpath):
                print('Read data from csv "' + str(csvpath) + '"')
                df = pd.read_csv(filepath_or_buffer=csvpath)
            else:
                s = """text,class,content_type
    hi how are you,hi,text
    yo my friend,hi,text
    cqcq anyone there,hi,text
    """
                print('Read data from string "' + str(s) + '"')
                df = pd.read_csv(StringIO(s), sep=',')
            records = df.to_dict('records')
            res = obj.add(records=records, tablename_or_index=ES_INDEX)
            print('Result for add as text: ' + str(res))
            # res = obj.add(records=df, tablename_or_index=ES_INDEX, doc_type='table')
            # print('Result for add as table: ' + str(res))
        elif mode == 'delete':
            res = obj.delete(match_phrase = {'label': 'hi'}, tablename_or_index=ES_INDEX)
            print('Result for delete..')
            print(res)
        else:
            pass

        mp = {"label": "hi"}
        rows = obj.get(match_phrase = mp, tablename_or_index=ES_INDEX, return_db_style_records=True)
        print('Query for match phrase: ' + str(mp))
        for row in rows:
            print(row)

        rows_scr = obj.get_all(
            tablename_or_index = ES_INDEX,
            max_records = 1,
            return_db_style_records = True,
            params_other = {'scroll': '5s'},
        )
        print('ALL rows (with scroll) from db index "' + str(ES_INDEX) + '"')
        [print(r) for r in rows_scr]

        rows = obj.get_all(
            tablename_or_index = ES_INDEX,
            max_records = 10000,
            return_db_style_records = True,
            params_other = {'csvpath': csvpath},
        )
        print('ALL rows from db index "' + str(ES_INDEX) + '"')
        [print(r) for r in rows]

        res = rows_scr == rows
        print('Result of scroll and non-scroll request, identical == ' + str(res))
        assert res, 'Scroll:\n\r' + str(rows_scr) + ', rows:\n\r' + str(rows)
        return

    def test(self):
        self.test_csv()
        # test_es()
        print('ALL TESTS PASSED OK')
        return


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    TestDataSources().test()
