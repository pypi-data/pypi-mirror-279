import logging
import time
import os
from opensearchpy import OpenSearch, NotFoundError
from nwae.math.datasource.DatastoreInterface import DatastoreInterface
import pandas as pd
from nwae.math.utils.Env import Env
from nwae.math.utils.EnvironRepo import EnvRepo
from nwae.math.utils.Logging import Logging


#
# > docker pull opensearchproject/opensearch:latest
# > docker run opensearchproject/opensearch:latest -p 9208:9200 \
#     -e "discovery.type=single-node" -e "add-host=host.docker.internal:host-gateway"
#
class OpenSearchDS(DatastoreInterface):

    # Elastic/Opensearch built-in max scroll rows by default is 10k, but on low-end machines will timeout, so put lower
    ES_BUILT_IN_MAX_ROWS = int(os.environ.get('OPENSEARCH_MAX_ROWS_PER_SCROLL', 500))

    # Default column name created by ES to store text embedding
    COL_TEXT_ENCODE = 'text_encode'

    def __init__(
            self,
            filepath = None,  # for CSV files data store
            logger = None,
            ignore_warnings = False,
            # connection options, can pass during connection or here
            host = None,
            port = None,
            username = None,
            password = None,
            database = None,
            # When data is written using Haystack library, normal queries won't work, don't know why
            # They must be adding lots of nonsense into it
            messed_by_haystack = False,
    ):
        super().__init__(
            filepath = filepath,
            logger = logger,
            ignore_warnings = ignore_warnings,
            host = host,
            port = port,
            username = username,
            password = password,
            database = database,
        )
        self.messed_by_haystack = messed_by_haystack
        # This env var will overwrite the default "DB_DEFAULT_TIMEOUT" in the class interface
        self.timeout = int(os.environ.get('OPENSEARCH_DEFAULT_TIMEOUT', self.timeout))

        self.logger.info('Opensearch max scroll rows set to ' + str(self.ES_BUILT_IN_MAX_ROWS))
        return

    def generate_query(
            self,
            key_values,
            cond_AND = True,
            exact_match = True,
    ):
        """
        Simple match phrases will not work with exact searches.
        This will cause the dangerous behaviour of deleting more data than desired.

        If for example you have these data
            {'label': 'xxx', 'len': 9,  'text': 'pineapple'},
            {'label': 'xxx', 'len': 10, 'text': 'pine apple'},
            {'label': 'xxx', 'len': 5,  'text': 'apple'}

        and you want to search (or delete) for text="apple", it will return (or delete) both these
            {'label': 'xxx', 'len': 10, 'text': 'pine apple'},
            {'label': 'xxx', 'len': 5,  'text': 'apple'}

        To make text searches exact, you must specify additional fields, or some ID, or use term search
        So if we search for len="5" & text="apple", then it will give you a single result you desire
            {'label': 'xxx', 'len': 5, 'text': 'apple'}
        or
        https://www.elastic.co/guide/en/elasticsearch/guide/current/_finding_exact_values.html#_term_query_with_text
        use term search as suggested in above link
            {'query': {'bool': {'must': {'term': {'text.keyword': 'apple'}}}}}
        """
        and_or = "must" if cond_AND else "should"

        if not self.messed_by_haystack:
            if exact_match:
                # https://stackoverflow.com/questions/21227492/elastic-search-query-for-multiple-conditions
                # Exact text match of this type, only for Elasticsearch version >= 8
                #    {"query": {"bool": {"must": {"term": {"text.keyword": text}}}}}
                # New one updated 2024-06-07
                #    {"query": {"bool": {"must": [{"term": {"col1.keyword": "abc"}}, {"term": {"col2.keyword": 123}}] }}}
                q = {
                    "query": {
                        "bool": {
                            and_or: [
                                { 'term': {k+'.keyword': v} } for k, v in key_values.items()
                                # 'term': {k + '.keyword': v for k, v in key_values.items()}
                            ]
                        }
                    }
                }
            else:
                match_phrases = []
                for k, v in key_values.items():
                    match_phrases.append({"match_phrase": {k: v}})
                q = {
                    "query": {
                        "bool": {and_or: match_phrases}
                    }
                }
        else:
            # When messed by Haystack, exact or non-exact search depends on column/key name.
            # If column is "text" it is always not exact, if column name is NOT "text", it will be exact.
            q = {"query": {"match_phrase": key_values}}
            have_text_column = "text" in key_values.keys()
            if have_text_column and exact_match:
                self.logger.warning(
                    'Column of name "text" cannot have exact search if messed by Haystack.'
                    + ' Using incorrect NON-EXACT query anyway: ' + str(q)
                )
            elif not exact_match:
                self.logger.warning(
                    'Column of name != "text" cannot have non-exact search if messed by Haystack.'
                    + ' Using incorrect EXACT query anyway: ' + str(q)
                )

        self.logger.info(
            'Using query for exact match "' + str(exact_match) + '", condition AND "' + str(cond_AND) + '":\n' + str(q)
        )

        return q

    def connect(
            self,
            host = None,
            port = None,
            username = None,
            password = None,
            database = None,
            scheme = 'https',
            # For our Soprano network, this must be False, otherwise too many problems with CA Authority
            verify_certs = True,
            other_params = None,
    ):
        host = self.host if host is None else host
        port = self.port if port is None else port
        username = self.username if username is None else username
        password = self.password if password is None else password

        for _ in [host, port, username, password]:
            assert _ is not None, 'Cannot be empty ' + str([host, port, username, password])

        url = str(scheme) + '://' + str(host) + ':' + str(port)
        self.logger.info(
            'Try connect to "' + str(url) + '", scheme "' + str(scheme) + '", verify ' + str(verify_certs)
        )

        self.con = OpenSearch(
            url,
            http_auth = (username, password),
            verify_certs = verify_certs,
            timeout = self.timeout,
            # max_retries = 1,
            # retry_on_timeout = False,
        )
        self.logger.info(
            'Connected successfully to "' + str(url) + '" using username "' + str(username)
            + '", default timeout ' + str(self.timeout) + 's.'
        )
        try:
            self.logger.info('Connection info: ' + str(self.con.info()))
        except Exception as ex:
            self.logger.error('Could not get info for connection "' + str(url) + '": ' + str(ex))
        return self.con

    def get(
            self,
            # e.g. {"answer": "take_seat"}
            match_phrase,
            tablename_or_index = None,
            return_db_style_records = True,
            request_timeout = 20.0,
            params_other = None,
    ):
        assert type(match_phrase) is dict
        params_other = {} if params_other is None else params_other

        prm_cond_and = params_other.get('cond_and', True)
        prm_exact_match = params_other.get('exact_match', True)

        query = self.generate_query(
            key_values = match_phrase,
            cond_AND = prm_cond_and,
            exact_match = prm_exact_match,
        )
        self.logger.debug(
            'Get/Query from index "' + str(tablename_or_index) + '", condition AND = ' + str(prm_cond_and)
            + ', exact match = ' + str(prm_exact_match) + ' for query ' + str(query)
        )
        try:
            resp = self.con.search(
                index = tablename_or_index,
                body = query,
                # OpenSearch ignores this and uses the one set in constructor class
                request_timeout = request_timeout,
            )
            self.logger.debug('Raw opensearch search response: ' + str(resp))
            rows = resp['hits']['hits']
            return [r['_source'] for r in rows] if return_db_style_records else rows
        except Exception:
            return []

    def get_all(
            self,
            key = None,
            max_records = 100000,
            tablename_or_index = None,
            return_db_style_records = True,
            request_timeout = 20.0,
            # supported values
            #   1. 'scroll' will force scrolling
            #   2. 'csvpath' will write data to csv path provided
            params_other = None,
    ):
        params_other = {} if params_other is None else params_other
        # Older 7.x version for elasticsearch pip does not support scroll
        user_force_scroll_secs = params_other.get('scroll', None)
        try:
            if key is not None:
                query_all = {"wildcard": {key: "*"}}
            else:
                query_all = {"match_all": {}}

            body = {
                "query": query_all,
                # Must not exceed built-in Elasticsearch max rows (or our defined value), else will throw exception
                "size": min(max_records, self.ES_BUILT_IN_MAX_ROWS),
            }

            if user_force_scroll_secs:
                self.logger.info(
                    'User force scroll. Elastic search query set in scroll mode, max records ' + str(max_records)
                )
                # body["scroll"] = user_force_scroll_secs
                scroll_param = str(user_force_scroll_secs) + 's'
                is_scroll_mode = True
            elif (max_records > self.ES_BUILT_IN_MAX_ROWS):
                # If user wants greater than built-in Elasticsearch max rows, we need to scroll for user
                self.logger.info(
                    'Elastic search query set in scroll mode, max records ' + str(max_records)
                    + ' exceed built-in ' + str(self.ES_BUILT_IN_MAX_ROWS)
                )
                # body["scroll"] = '5s'
                scroll_param = '1m'
                is_scroll_mode = True
            else:
                scroll_param = None
                is_scroll_mode = False

            self.logger.info(
                'Sending query to Elasticsearch index "' + str(tablename_or_index) + '", scroll = ' + str(is_scroll_mode)
                + ': ' + str(body)
            )
            scroll_count = 1
            if is_scroll_mode:
                # Unlike ElasticSearch that passes the "scroll" key to the body,
                # OpenSearch passes it directly to function
                resp = self.con.search(
                    index = tablename_or_index,
                    body = body,
                    scroll = scroll_param,
                    # OpenSearch ignores this and uses the one set in constructor class
                    request_timeout = request_timeout,
                )
            else:
                resp = self.con.search(
                    index = tablename_or_index,
                    body = body,
                    # OpenSearch ignores this and uses the one set in constructor class
                    request_timeout = request_timeout,
                )

            self.logger.info(
                'Response from OpenSearch with keys: ' + str(resp.keys())
                + ', timed out = ' + str(resp.get('timed_out', None))
            )
            rows = resp['hits']['hits']
            scroll_id = resp['_scroll_id'] if is_scroll_mode else None
            self.logger.info(
                'Rows from scroll count #' + str(scroll_count) + ' length ' + str(len(rows)) + ', scroll id "'
                + str(scroll_id) + '"'
            )

            while scroll_id is not None:
                scroll_count += 1
                self.logger.debug(
                    'Scroll mode, making subsequent request #' + str(scroll_count)
                    + ', scroll id "' + str(scroll_id) + '"'
                )
                resp = self.con.scroll(
                    scroll_id = scroll_id,
                    scroll = scroll_param,
                    # scroll = body["scroll"],
                    # OpenSearch ignores this and uses the one set in constructor class
                    request_timeout = request_timeout,
                )
                # scroll_id = resp['_scroll_id'] if is_scroll_mode else None
                rows_scroll = resp['hits']['hits']
                if len(rows_scroll) == 0:
                    self.logger.info('Length of scroll rows already 0: ' + str(rows_scroll))
                    scroll_id = None
                else:
                    self.logger.info(
                        'Scroll #' + str(scroll_count) + ' append ' + str(len(rows_scroll))
                        + ' row(s) to running rows of length ' + str(len(rows))
                    )
                    rows = rows + rows_scroll

            records_db_style = [r['_source'] for r in rows]
            csvpath = params_other.get('csvpath', None)
            if csvpath is not None:
                try:
                    df = pd.DataFrame(data=records_db_style)
                    df.to_csv(path_or_buf=csvpath, index=False)
                except Exception as ex_csv:
                    raise Exception('Error writing to csv path "' + str(csvpath) + '", exception ' + str(ex_csv))
            return records_db_style if return_db_style_records else rows
        except NotFoundError as ex_nf:
            errmsg = 'Error get records for key "' + str(key) + '", tablename/index "' \
                     + str(tablename_or_index) + '", exception type "' + str(type(ex_nf)) + '": ' + str(ex_nf)
            self.logger.error(errmsg)
            # if table/index not exist, just return empty
            return []
        except Exception as ex:
            errmsg = 'Error get records for key "' + str(key) + '", tablename/index "' \
                     + str(tablename_or_index) + '", exception type "' + str(type(ex)) + '": ' + str(ex)
            self.logger.error(errmsg)
            # raise exception for anything else
            raise ex

    def get_indexes(self):
        indices = self.con.indices.get(index='*')
        self.logger.info('Returned indices')
        [self.logger.debug('Index "' + str(key) + '": ' + str(row)) for key, row in indices.items()]
        return [idx for idx in indices.keys()]

    def delete_index(
            self,
            tablename_or_index,
    ):
        self.logger.warning('Deleting index "' + str(tablename_or_index) + '"...')
        res = self.con.indices.delete(index=tablename_or_index)
        self.logger.warning('Deleted index "' + str(tablename_or_index) + '" with returned result: ' + str(res))
        # make sure return as type "dict" (.body) instead of type "elastic_transport.ObjectApiResponse"
        return res

    def get_mapping(
            self,
            tablename_or_index = None,
    ):
        try:
            res = self.con.indices.get_mapping(index=tablename_or_index)
            return res
        except Exception as ex:
            self.logger.error('Error get mapping for index "' + str(tablename_or_index) + '": ' + str(ex))
            return None

    def add(
            self,
            # list of dicts
            records,
            tablename_or_index = None,
            params_other = None,
    ):
        res_list = []
        for rec in records:
            res = self.con.index(
                index = tablename_or_index,
                body = rec,
                # doc_type = doc_type,
                # id = str(uuid.uuid4()) if doc_id is None else doc_id,
            )
            body = res
            self.logger.debug('Result add (type "' + str(type(body)) + '"): ' + str(body))
            # make sure return as type "dict" (.body) instead of type "elastic_transport.ObjectApiResponse"
            res_list.append(body)
        return res_list

    def delete(
            self,
            match_phrase,
            tablename_or_index = None,
            params_other = None,
    ):
        assert type(match_phrase) is dict
        query = self.generate_query(
            key_values = match_phrase,
            cond_AND = True,
            # for delete(), always exact match
            exact_match = True,
        )

        self.logger.debug('Deleting from index "' + str(tablename_or_index) + '" for query ' + str(query))
        res = self.con.delete_by_query(
            index = tablename_or_index,
            body = query,
        )
        self.logger.debug('Delete result from opensearch: ' + str(res))
        # make sure return as type "dict" (.body) instead of type "elastic_transport.ObjectApiResponse"
        return res

    def delete_by_raw_query(
            self,
            raw_query,
            tablename_or_index = None,
            params_other = None,
    ):
        self.logger.debug('Deleting from index "' + str(tablename_or_index) + '" for query ' + str(raw_query))
        res = self.con.delete_by_query(
            index = tablename_or_index,
            body = raw_query,
        )
        self.logger.debug('Delete result from opensearch: ' + str(res))
        # make sure return as type "dict" (.body) instead of type "elastic_transport.ObjectApiResponse"
        return res

    def delete_all(
            self,
            key,
            tablename_or_index = None,
    ):
        rows = self.get_all(
            key = key,
            tablename_or_index = tablename_or_index,
            return_db_style_records = True,
        )
        values = list({row[key] for row in rows})
        self.logger.info('Unique values for key "' + str(key) + '" to be deleted: ' + str(values))
        if len(values) == 0:
            return None
        else:
            deleted_results = []
            for val in values:
                match_phrase = {key: val}
                res = self.delete(
                    match_phrase = match_phrase,
                    tablename_or_index = tablename_or_index,
                )
                # some returned objects are not JSON serializable, so return as string instead
                deleted_results.append(res)
                self.logger.debug('Deleted match phrase ' + str(match_phrase) + ', res: ' + str(res))
            return deleted_results

    def add_column(
            self,
            colnew,
            data_type = str,
            tablename_or_index = None,
            default_value = None,
    ):
        records = self.get_all(
            max_records = 1000000,
            tablename_or_index = tablename_or_index,
            return_db_style_records = True,
        )
        for r in records:
            r[colnew] = default_value
            self.delete(
                match_phrase = {'text': r['text']},
                tablename_or_index = tablename_or_index,
            )
            self.add(
                records = [r],
                tablename_or_index = tablename_or_index,
            )
            self.logger.debug(
                'Added new record with new column ' + str(r)
            )
        self.logger.info(
            'Done adding new column "' + str(colnew) + '" using default value "' + str(default_value)
            + '", total rows = ' + str(len(records))
        )


if __name__ == '__main__':
    er = EnvRepo(repo_dir=os.environ["REPO_DIR"])
    Env.set_env_vars_from_file(env_filepath=er.REPO_DIR + '/.env.bash.ubinlp.opensearch')

    db_index = 'metadata'

    es = OpenSearchDS(
        ignore_warnings = True,
        logger = Logging.get_default_logger(log_level=logging.INFO, propagate=False)
    )
    es.connect(
        host = os.environ["DB_HOST"],
        port = os.environ["DB_PORT"],
        username = os.environ["DB_USERNAME"],
        password = os.environ["DB_PASSWORD"],
        scheme = os.environ["DB_SCHEME"],
        verify_certs = False,
    )

    all_recs = [
        {k: v for k, v in r.items() if k != 'embedding'} for r in
        es.get_all(tablename_or_index=db_index)
    ]
    [print(i, r) for i, r in enumerate(all_recs)]

    match_phrase = {
        "metadata_index": 'en-faq_test_1',
        "metadata_identifier": "lastUpdateTime"
    }
    rows = es.get(
        match_phrase = match_phrase,
        tablename_or_index = db_index,
    )
    print(rows)
    print('----------------------------------------------------------------')
    print(rows)
    [print(i, r) for i, r in enumerate(rows)]
    exit(0)
    # if idx_map is not None:
    #     print('** Root Keys', idx_map[db_index].keys())
    #     print('** Mapping Keys', idx_map[db_index]['mappings'].keys())
    #     print('** Mapping/Properties Keys', idx_map[db_index]['mappings']['properties'].keys())
    #     print('** Property List')
    #     d = idx_map[db_index]['mappings']['properties']
    #     [print('   ', i, k, v) for i, (k, v) in enumerate(d.items())]
    #
    #     print(es.get_all(key='content', tablename_or_index=db_index))
    #     exit(0)

    # try: es.delete_index(tablename_or_index=db_index)
    # except: pass

    es.add(
        records = [{'id': 1}, {'id': 2}],
        tablename_or_index = db_index,
    )
    time.sleep(2)
    print('***** get_all() *****')
    print(es.get_all(tablename_or_index=db_index, request_timeout=1.0))
    exit(0)

    for em in (True, False,):
        res = es.get(
            match_phrase = {'id': 1},
            tablename_or_index = db_index,
            params_other = {'exact_match': em, 'cond_and': True},
        )
        print('***** get() using exact match = ' + str(em))
        print(res)

    es.delete(
        match_phrase = {'id': 1},
        tablename_or_index = db_index,
    )

    time.sleep(2)
    print('***** get_all() *****')
    print(es.get_all(tablename_or_index=db_index))

    # es.delete_index(tablename_or_index=db_index)
    exit(0)
