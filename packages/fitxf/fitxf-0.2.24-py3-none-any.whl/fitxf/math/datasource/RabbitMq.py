import logging
import threading
import pika
import time
import sys
import msgpack
from nwae.math.utils.DatastoreInterface import DatastoreInterface


#
# Simple local setup
#   > docker pull rabbitmq
#   > docker run -d -p 5672:5672 --hostname my-rabbit --name some-rabbit rabbitmq
# Done. RabbitMQ now running with default username/password 'guest'/'guest' on port 5672
#
class RabbitMq(DatastoreInterface):

    PARAM_QUEUE_CONSUME = 'queue_consume'
    PARAM_QUEUE_REPLY = 'queue_reply'
    PARAM_DURABLE = 'durable'

    def __init__(
            self,
            filepath = None,    # for CSV files data store
            logger = None,
            ignore_warnings = False,
            # connection options, can pass during connection or here
            host = None,
            port = None,
            username = None,
            password = None,
            database = None,
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
        self.threads = []
        self.signal_stop_threads = False

        # Handle signals
        try:
            import signal
            signal.signal(signal.SIGINT, self.stop_threads)
            signal.signal(signal.SIGTERM, self.stop_threads)
        except Exception as ex:
            self.logger.error('Error initializing signal handlers: ' + str(ex))
        return

    def stop_threads(
            self,
            sig = None,
            frame = None,
    ):
        self.logger.info('Signal received "' + str(sig) + '", frame "' + str(frame) + '"')
        self.signal_stop_threads = True
        self.logger.info('Stop thread command received. Total threads to stop = ' + str(len(self.threads)) + '.')
        for thr in self.threads:
            self.logger.info('Stopping thread "' + str(thr.name) + '"')
            thr.join()
        self.logger.info('All threads successfully stopped')
        return

    def connect(
            self,
            host     = None,
            port     = None,
            username = None,
            password = None,
            database = None,
            scheme   = None,
            # For our Soprano network, this must be False, otherwise too many problems with CA Authority
            verify_certs = True,
            other_params = None,
    ):
        try:
            # use same mutex for write
            self.mutex_write.acquire()

            self.conn_host = host
            self.conn_port = port
            self.conn_username = username
            self.conn_password = password
            self.conn_other_params = other_params

            self.conn_forever = self.conn_other_params.get('forever', True)

            vh = self.conn_other_params.get('virtual_host', None)
            vh = None if str(vh).strip()=='' else vh

            if vh is not None:
                conn_params = pika.ConnectionParameters(
                    host = self.conn_host,
                    port = self.conn_port,
                    virtual_host = self.conn_other_params['virtual_host'],
                    credentials = pika.PlainCredentials(username=self.conn_username, password=self.conn_password),
                )
            else:
                conn_params = pika.ConnectionParameters(
                    host = self.conn_host,
                    port = self.conn_port,
                    credentials = pika.PlainCredentials(username=self.conn_username, password=self.conn_password),
                )

            self.connection = pika.BlockingConnection(conn_params)
            self.logger.info(
                'Connection to RabbitMq successful. Host "' + str(self.conn_host) + '", port "' + str(self.conn_port)
                + '", username "' + str(self.conn_username) + '", password "****' + str(self.conn_password[-4:])
                + '", forever = ' + str(self.conn_forever)
            )
            self.channel = self.connection.channel()
            self.logger.info(
                'Channel also successfully formed to RabbitMq successful. Host "' + str(self.conn_host)
                + '", port "' + str(self.conn_port)
                + '", username "' + str(self.conn_username) + '", password "****' + str(self.conn_password[-4:])
                + '", forever = ' + str(self.conn_forever)
            )
            return True
        except Exception as ex:
            self.logger.error(
                'Error connecting or creating channel to RabbitMq. Host "' + str(self.conn_host)
                + '", port "' + str(self.conn_port)
                + '", username "' + str(self.conn_username) + '", password "****' + str(self.conn_password[-4:])
                + '": ' + str(ex)
            )
            return False
        finally:
            self.mutex_write.release()

    def declare_queue_with_reconnect_forever(
            self,
            queue_name,
            durable,
    ):
        sleep_time = 5
        while True:
            if self.signal_stop_threads:
                self.logger.info('Signal stop thread set, exiting infinite loop..')
                break
            try:
                self.channel.queue_declare(queue=queue_name, durable=durable)
                self.logger.info('Successfully declared queue "' + str(queue_name) + '"')
                return True
            # except (ConnectionClosed, StreamLostError) as ex_conn_closed:
            except Exception as ex_any:
                self.logger.error(
                    'Exception declaring queue "' + str(queue_name) + '" to host "'
                    + str(self.conn_host) + '": ' + str(ex_any)
                )
                time.sleep(sleep_time)

                if not self.conn_forever:
                    break
                self.logger.info('Trying to reconnect...')
                ok = self.connect(
                    host = self.conn_host,
                    port = self.conn_port,
                    username = self.conn_username,
                    password = self.conn_password,
                    other_params = self.conn_other_params,
                )
                if ok:
                    self.logger.info('Successfully reconnected to host "' + str(self.conn_host) + '"')
                else:
                    self.logger.error(
                        'Failed to connect to host "' + str(self.conn_host) + '". Will try again in ' + str(sleep_time)
                        + 's..'
                    )

    def set_receive_callback(
            self,
            callback,
            other_params = None
    ):
        assert 'queue_consume' in other_params.keys()
        queue_consume = other_params['queue_consume']
        durable = other_params.get(self.PARAM_DURABLE, False)

        def background_receive_forever():
            while True:
                self.declare_queue_with_reconnect_forever(queue_name=queue_consume, durable=durable)
                self.logger.info(
                    'Set callback for consuming in queue "' + str(queue_consume) + '" to function ' + str(callback)
                )
                self.channel.basic_consume(
                    queue = queue_consume,
                    auto_ack = True,
                    on_message_callback = callback,
                )
                self.logger.info(
                    'Basic consume successfully called in consume queue "' + str(queue_consume)
                    + '", entering blocking call start_consuming()...'
                )
                try:
                    # This is a blocking call and will not return unless connection is broken
                    self.channel.start_consuming()
                except Exception as ex:
                    self.logger.error(
                        'Channel consuming broken in queue "' + str(queue_consume) + '" exception: ' + str(ex)
                    )
            # Should never come here
            self.logger.critical('DONE with background receive!!')

        bg = threading.Thread(
            target = background_receive_forever,
            name = 'consume on ' + str(queue_consume),
            args = [],
        )
        bg.start()
        self.threads.append(bg)
        self.logger.info(
            'Thread "' + str(bg.name) + '" to consume/receive on queue "' + str(queue_consume) + '" started...'
        )
        return

    def get(
            self,
            # e.g. {"answer": "take_seat"}
            match_phrase,
            # RabbitMq queue name
            tablename_or_index = None,
            request_timeout = 20.0,
            params_other = None,
    ):
        raise Exception(
            'In RabbitMq, there is no read/get data, instead you have to implement a callback and call '
            'set_receive_callback()'
        )

    def get_all(
            self,
            key = None,
            max_records = 10000,
            tablename_or_index = None,
            return_db_style_records  =True,
            request_timeout = 20.0,
            params_other = None,
    ):
        raise Exception(
            'In RabbitMq, there is no read/get data, instead you have to implement a callback and call '
            'set_receive_callback()'
        )

    def get_indexes(self):
        return 'This function not supported'

    def delete_index(
            self,
            tablename_or_index,
    ):
        return 'This function not supported'

    def add(
            self,
            # list of dicts
            records,
            tablename_or_index = None,
            params_other = None,
    ):
        params_other = {} if params_other is None else params_other
        durable = params_other.get(self.PARAM_DURABLE, False)

        queue_name = tablename_or_index
        self.declare_queue_with_reconnect_forever(queue_name=queue_name, durable=durable)
        for rec in records:
            try:
                self.channel.basic_publish(
                    exchange = '',
                    routing_key = queue_name,
                    body = msgpack.packb(rec, use_bin_type=True)
                )
                self.logger.debug('Successfully published to queue "' + str(queue_name) + '"')
            except Exception as ex:
                self.logger.error(
                    'Exception publishing to queue "' + str(queue_name) + '": ' + str(ex)
                    + ' Data meant to be written to queue : ' + str(rec)
                )
        return

    def delete(
            self,
            match_phrase,
            tablename_or_index = None,
            params_other = None,
    ):
        raise Exception('In RabbitMq, there is no delete data')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    local_rabbitmq = True
    queue_read = 'sms_cdr_cleanup'
    queue_write = 'sms_cdr_test'
    test_packet = {'text': 'Email asdf@asdf.com phone +380969265555 ok'}

    def example_callback(ch, method, properties, body):
        # body_str = body.decode()
        body_unpacked = msgpack.unpackb(body, raw=False, strict_map_key=False)
        logging.info(
            '***** Received from channel:'
            # + '\n  --> ' + str(ch)
            # + '", method "' + str(method)
            # + '", properties:\n' + str(properties)
            + ' body type "' + str(type(body)) + '" convert to type "' + str(type(body_unpacked))
            + '": ' + str(body_unpacked)
        )

    ds_write = RabbitMq()
    ds_read = RabbitMq()

    for ds in [ds_write, ds_read]:
        other_params = {'forever': True} if local_rabbitmq else {'virtual_host': '/platform', 'forever': True, }
        ds.connect(
            host = 'localhost' if local_rabbitmq else '',
            port = '5672',
            username = 'guest' if local_rabbitmq else '',
            password = 'guest' if local_rabbitmq else '',
            other_params = other_params,
        )
    ds_read.set_receive_callback(
        callback = example_callback,
        other_params = {
            RabbitMq.PARAM_QUEUE_CONSUME: queue_write,
        },
    )

    while True:
        sys.stdout.write("% ")
        s = input()
        if s.strip() in ('',):
            continue
        if s.strip().lower() in ('quit', 'exit',):
            break
        print('Writing "' + str(s) + '" to queue "' + str(queue_read) + '"')
        test_packet['body'] = s
        ds_write.add(
            records = [test_packet],
            tablename_or_index = queue_read,
        )
    ds.connection.close()
    exit(0)
