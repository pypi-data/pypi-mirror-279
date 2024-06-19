import logging
import time
import os
from elasticsearch import Elasticsearch, NotFoundError
from nwae.math.datasource.DatastoreInterface import DatastoreInterface
import pandas as pd
from nwae.math.utils.PkgVersion import PkgVersion


"""
To reset password on Docker ElasticSearch 8.x
  > docker exec -it es01 /usr/share/elasticsearch/bin/elasticsearch-reset-password -u elastic
or go inside Container CLI
  > cd /usr/share/elasticsearch/bin/
  > ./elasticsearch-reset-password -u elastic
  
For Elasticsearch 7.x, default password is "changeme", and you can test via
  > curl -u elastic:changeme http://localhost:9200
"""
class ES(DatastoreInterface):

    # Elastic/Opensearch built-in max scroll rows by default is 10k, but on low-end machines will timeout, so put lower
    ES_BUILT_IN_MAX_ROWS = int(os.environ.get('OPENSEARCH_MAX_ROWS_PER_SCROLL', 500))

    # Default column name created by ES to store text embedding
    COL_TEXT_ENCODE = 'text_encode'

    def __init__(
            self,
            filepath = None,  # for CSV files data store
            logger   = None,
            ignore_warnings = False,
            # connection options, can pass during connection or here
            host     = None,
            port     = None,
            username = None,
            password = None,
            database = None,
            # When data is written using Haystack library, normal queries won't work, don't know why
            # They must be adding lots of nonsense into it
            messed_by_haystack = False,
    ):
        super().__init__(
            filepath = filepath,
            logger   = logger,
            ignore_warnings = ignore_warnings,
            host     = host,
            port     = port,
            username = username,
            password = password,
            database = database,
        )
        self.messed_by_haystack = messed_by_haystack
        self.is_elasticsearch_old_ver, self.curver = PkgVersion().check_package_version(
            pkg_name = 'elasticsearch',
            # Major version 8 onwards uses "body" instead of "document"
            version  = '7',
            return_version = True,
        )
        # This env var will overwrite the default "DB_DEFAULT_TIMEOUT" in the class interface
        self.timeout = int(os.environ.get('OPENSEARCH_DEFAULT_TIMEOUT', self.timeout))
        self.logger.info(
            'Pip elasticsearch version "' + str(self.curver) + '", is old version = '
            + str(self.is_elasticsearch_old_ver)
        )
        return

    def is_elastic_server_version_8_x_or_above(self):
        es_ver = str(self.con.info()['version']['number']).split(sep='.')
        es_server_is_ver_8_x_or_above = int(es_ver[0]) >= 8
        self.logger.debug(
            'Connected elastic search version ' + str(es_ver) + ', is >8.x = ' + str(es_server_is_ver_8_x_or_above)
        )
        return es_server_is_ver_8_x_or_above

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
                # Exact text match of this type, only for Elasticsearch version >= 8
                #    {"query": {"bool": {"must": {"term": {"text.keyword": text}}}}}
                q = {
                    "query": {
                            "bool": {
                                    and_or: {
                                        'term': {k+'.keyword':v for k,v in key_values.items()}
                                    }
                            }
                    }
                }
            else:
                match_phrases = []
                for k, v in key_values.items():
                    match_phrases.append({"match_phrase": {k: v}})
                q = {
                    "query": {
                        "bool": { and_or: match_phrases }
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
            host     = None,
            port     = None,
            username = None,
            password = None,
            database = None,
            scheme   = 'https',
            # For our Soprano network, this must be False, otherwise too many problems with CA Authority
            verify_certs = True,
            other_params = None,
    ):
        host = self.host if host is None else host
        port = self.port if port is None else port
        username = self.username if username is None else username
        password = self.password if password is None else password

        for _ in [host, port, username, password]:
            assert _ is not None, 'Cannot be empty'

        url = str(scheme) + '://' + str(host) + ':' + str(port)
        self.logger.info(
            'Try connect to "' + str(url) + '", scheme "' + str(scheme) + '", verify ' + str(verify_certs)
        )

        if not self.is_elasticsearch_old_ver:
            self.con = Elasticsearch(
                url,
                basic_auth = (username, password),
                verify_certs = verify_certs,
                timeout = self.timeout,
            )
            self.logger.info(
                'Connected successfully to "' + str(url) + '" using username "' + str(username)
                + '", default timeout ' + str(self.timeout) + 's.'
            )
        else:
            self.con = Elasticsearch(
                [host],
                port      = port,
                http_auth = (username, password),
                scheme    = scheme,
                use_ssl   = True if scheme=='https' else False,
                verify_certs = verify_certs,
            )
        try:
            self.logger.debug(self.con.info())
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
        resp = self.con.search(
            index = tablename_or_index,
            body  = query,
            request_timeout = request_timeout,
        )
        self.logger.debug('Raw elasticsearch search response: ' + str(resp))
        try:
            rows = resp['hits']['hits']
            return [r['_source'] for r in rows] if return_db_style_records else rows
        except Exception:
            return []

    """
    In ES there is no such thing as "SELECT * FROM ..."
    But we hack up a way anyway
    """

    def get_all(
            self,
            key         = None,
            max_records = ES_BUILT_IN_MAX_ROWS,
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
        user_force_scroll_secs = None if self.is_elasticsearch_old_ver else params_other.get('scroll', None)
        try:
            if key is not None:
                query_all = {"wildcard": {key: "*"}}
            else:
                query_all = {"match_all": {}}

            body = {
                "query": query_all,
                # Must not exceed built-in Elasticsearch max rows, else will throw exception
                "size":  min(max_records, self.ES_BUILT_IN_MAX_ROWS),
            }

            if user_force_scroll_secs:
                self.logger.info(
                    'User force scroll. Elastic search query set in scroll mode, max records ' + str(max_records)
                )
                body["scroll"] = user_force_scroll_secs
                is_scroll_mode = True
            elif (not self.is_elasticsearch_old_ver) and (max_records > self.ES_BUILT_IN_MAX_ROWS):
                # If user wants greater than built-in Elasticsearch max rows, we need to scroll for user
                self.logger.info(
                    'Elastic search query set in scroll mode, max records ' + str(max_records)
                    + ' exceed built-in ' + str(self.ES_BUILT_IN_MAX_ROWS)
                )
                body["scroll"] = '5s'
                is_scroll_mode = True
            else:
                is_scroll_mode = False

            self.logger.info(
                'Sending query to Elasticsearch index "' + str(tablename_or_index) + '" ' + str(body)
            )
            scroll_count = 1
            resp = self.con.search(
                index = tablename_or_index,
                body  = body,
                request_timeout = request_timeout,
            )
            self.logger.debug('Response from Elasticsearch all query: ' + str(resp))
            rows = resp['hits']['hits']
            self.logger.debug(
                'Rows from scroll count #' + str(scroll_count) + ' length ' + str(len(rows))
                + ': ' + str(rows)
            )
            scroll_id = resp['_scroll_id'] if is_scroll_mode else None

            while scroll_id is not None:
                scroll_count += 1
                self.logger.debug(
                    'Scroll mode, making subsequent request #' + str(scroll_count)
                    + ', scroll id "' + str(scroll_id) + '"'
                )
                resp = self.con.scroll(
                    scroll_id = scroll_id,
                    scroll    = body["scroll"],
                    request_timeout = request_timeout,
                )
                scroll_id = resp['_scroll_id'] if is_scroll_mode else None
                rows_scroll = resp['hits']['hits']
                self.logger.debug(
                    'Rows from scroll count #' + str(scroll_count) + ' length ' + str(len(rows_scroll))
                    + ': ' + str(rows_scroll)
                )
                if len(rows_scroll) == 0:
                    self.logger.debug('Length of scroll rows already 0: ' + str(rows_scroll))
                    scroll_id = None
                else:
                    self.logger.debug(
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
        if self.is_elasticsearch_old_ver:
            res = self.con.indices.delete(index=tablename_or_index)
        else:
            res = self.con.options(ignore_status=[400, 404]).indices.delete(
                index=tablename_or_index,
            )
        self.logger.warning('Deleted index "' + str(tablename_or_index) + '" with returned result: ' + str(res))
        # make sure return as type "dict" (.body) instead of type "elastic_transport.ObjectApiResponse"
        if self.is_elasticsearch_old_ver:
            return res
        else:
            return res.body

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
            # doc_type = '_doc',
            # doc_id   = None,
            tablename_or_index = None,
            params_other = None,
    ):
        res_list = []
        for rec in records:
            if self.is_elasticsearch_old_ver:
                res = self.con.index(
                    index = tablename_or_index,
                    body = rec,
                    # doc_type = doc_type,
                    # id = str(uuid.uuid4()) if doc_id is None else doc_id,
                )
            else:
                res = self.con.index(
                    index = tablename_or_index,
                    document = rec,
                    # doc_type = doc_type,
                    # id       = str(uuid.uuid4()) if doc_id is None else doc_id,
                )
                res = res.body
            self.logger.debug('Result add (type "' + str(type(res)) + '"): ' + str(res))
            # make sure return as type "dict" (.body) instead of type "elastic_transport.ObjectApiResponse"
            res_list.append(res)
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
        self.logger.debug('Delete result from elasticsearch: ' + str(res))
        # make sure return as type "dict" (.body) instead of type "elastic_transport.ObjectApiResponse"
        return res.body if not self.is_elasticsearch_old_ver else res

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
    logging.basicConfig(level=logging.INFO)

    db_index = 'test_index'
    es = ES()
    es.connect(
        host = 'localhost',
        port = 9208,
        username = 'elastic',
        password = 'xcYF*atYc7gZ5ZLqStXi',
        # password = 'QNJ8xpGE29rEnQ_8s+9H',
        scheme = 'https',
        verify_certs = False,
    )
    es.delete_index(tablename_or_index=db_index)
    es.add(
        records = [{'id': 1}, {'id': 2}],
        tablename_or_index = db_index,
    )
    time.sleep(2)
    print(es.get_all(tablename_or_index=db_index))
    es.delete_index(tablename_or_index=db_index)
    exit(0)
