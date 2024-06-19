import logging
import time
import re
import os
from nwae.math.datasource.OpenSearch import OpenSearchDS
from nwae.math.datasource.ElasticSearch import ES
from nwae.math.utils.Logging import Logging
from nwae.math.utils.Env import Env
from nwae.math.utils.EnvironRepo import EnvRepo


class EsUnitTest:

    NAME_ELASTICSEARCH = 'elasticsearch'
    NAME_OPENSEARCH = 'opensearch'

    def __init__(
            self,
            logger = None,
    ):
        self.logger = logger if logger is not None else logging.getLogger()
        return

    def test(self):
        self.db_type = os.environ["DB_TYPE"]
        self.search_obj = ES if self.db_type == self.NAME_ELASTICSEARCH else OpenSearchDS
        print('Using search object class type: ' + str(self.search_obj))
        INTENDED_ES_SERVER_VERSION = 8

        self.es_obj = self.search_obj(
            ignore_warnings = True,
            messed_by_haystack = False,
            logger = self.logger,
        )
        self.es_obj.connect(
            host = os.environ["DB_HOST"],
            port = os.environ["DB_PORT"],
            username = os.environ["DB_USERNAME"],
            password = os.environ["DB_PASSWORD"],
            scheme = os.environ["DB_SCHEME"],
            verify_certs = False,
        )

        # Make sure connected server has same version as version intended
        es_ver = str(self.es_obj.con.info()['version']['number']).split(sep='.')
        print('Connected <' + str(self.db_type) + '> version:', es_ver)
        if self.db_type == self.NAME_ELASTICSEARCH:
            assert int(es_ver[0]) == INTENDED_ES_SERVER_VERSION, 'Connected version ' + str(es_ver) + ' not intended'

        #
        # Start Testing
        #
        tablename_or_index = 'en-es_unittest'
        col_ref = 'text'
        test_text = "US green apple"
        key_values_match = {col_ref: test_text}
        # key_values_non_exact_match_text_old_version = {'text': test_text}

        try: self.es_obj.delete_index(tablename_or_index=tablename_or_index)
        except: pass
        # self.es_obj.delete_all(
        #     key = col_ref,
        #     tablename_or_index = tablename_or_index,
        # )
        # sleep a while for slow Elasticsearch to reflect result
        time.sleep(2)
        res = self.es_obj.get_all(
            tablename_or_index = tablename_or_index,
            return_db_style_records = True,
        )
        print('--------- ALL Result in DB after delete index "' + str(tablename_or_index) + '"')
        print(res)
        assert len(res) == 0, 'After delete all, length data in DB should be 0, but got ' + str(len(res))

        test_data = [
            {'label': 'xxx', col_ref: 'pineapple'},
            {'label': 'xxx', col_ref: 'pine ' + test_text},
            {'label': 'xxx', col_ref: test_text},
            {'label': 'xxx', col_ref: test_text},
            {'label': 'xxx', col_ref: test_text + '?'},
            # should not be the same, if all uppercase/lowercase
            {'label': 'xxx', col_ref: test_text.upper()},
            {'label': 'xxx', col_ref: test_text.lower()},
        ]
        len_test_text_exact, len_test_text_non_exact = 0, 0
        for r in test_data:
            if r[col_ref] == test_text:
                len_test_text_exact += 1
            if re.search(pattern=test_text, string=r[col_ref], flags=re.IGNORECASE):
                len_test_text_non_exact += 1
        print('Exact matches for "' + str(test_text) + '" = ' + str(len_test_text_exact))
        print('Non-exact matches for "' + str(test_text) + '" = ' + str(len_test_text_non_exact))

        for rec in test_data:
            # add a "text" column if reference column is not "text"
            if col_ref != 'text':
                rec['text'] = rec[col_ref]
            res = self.es_obj.add(
                records = [rec],
                tablename_or_index = tablename_or_index,
            )
            print('For record ' + str(rec) + ' add result: ' + str(res))

        # sleep a while for slow Elasticsearch to reflect result
        time.sleep(2)
        res = self.es_obj.get_all(
            tablename_or_index = tablename_or_index,
            return_db_style_records = True,
        )
        print('--------- ALL Result in DB after add data')
        print(res)
        assert len(res) == len(test_data), \
            'After add all data, data length should be ' + str(len(test_data)) + ' but got ' + str(len(res))

        #
        # Test exact search
        #
        res = self.es_obj.get(
            match_phrase = key_values_match,
            tablename_or_index = tablename_or_index,
            return_db_style_records = True,
            params_other = {'exact_match': True},
        )
        print('--------- "' + test_text + '" Result exact search "' + str(test_text) + '" in DB')
        print(res)
        assert len(res) == len_test_text_exact, \
            'Exact search result for "' + str(test_text) + '" should be ' + str(len_test_text_exact) \
            + ' but got ' + str(len(res))
        for r in res:
            assert r[col_ref] == test_text, \
                'Exact search for "' + str(test_text) + '" got inexact result "' + str(r[col_ref]) + '"'

        #
        # Test non-exact search
        #
        res = self.es_obj.get(
            match_phrase = key_values_match, #if self.is_new_elasticsearch_server_ver8 else key_values_non_exact_match_text_old_version,
            tablename_or_index = tablename_or_index,
            return_db_style_records = True,
            params_other = {'exact_match': False},
        )
        print('--------- "' + test_text + '" Result non-exact search "' + str(test_text) + '" in DB')
        print(res)
        assert len(res) == len_test_text_non_exact, \
            'Non exact search should return length ' + str(len_test_text_non_exact) \
            + ', but got ' + str(len(res)) + ': ' + str(res)
        for r in res:
            assert re.search(pattern=test_text, string=r[col_ref], flags=re.IGNORECASE), \
                'Inexact search for "' + str(test_text) + '" returned wrongly "' + str(r[col_ref]) + '"'

        res = self.es_obj.delete(
            match_phrase = key_values_match,
            tablename_or_index = tablename_or_index,
        )
        print('Delete result for ' + str(key_values_match) + ': ' + str(res))
        assert res['deleted'] == len_test_text_exact, \
            'Exact delete search should be ' + str(len_test_text_exact) + ' but got ' + str(res['deleted'])
        # sleep a while for slow Elasticsearch to reflect result
        time.sleep(2)

        res = self.es_obj.get_all(
            tablename_or_index = tablename_or_index,
            return_db_style_records = True,
        )
        print('--------- ALL Result in DB after (exact) deletion(s)')
        print(res)
        count_remain = len(test_data) - len_test_text_exact
        assert len(res) == count_remain, \
            'Data count in DB should be ' + str(count_remain) + ' but got ' + str(len(res))

        print('ALL TESTS PASSED OK')
        return


if __name__ == '__main__':
    er = EnvRepo(repo_dir=os.environ["REPO_DIR"])
    Env.set_env_vars_from_file(env_filepath=er.REPO_DIR + '/.env.bash.ubinlp.opensearch')

    EsUnitTest(logger=Logging.get_default_logger(log_level=logging.INFO, propagate=False)).test()
    exit(0)
