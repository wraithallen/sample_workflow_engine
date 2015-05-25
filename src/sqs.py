
import boto.sqs
from time import sleep
from boto.sqs.message import Message
from configutil import get_config
from logutil import get_logger

_config = get_config()
_logger = get_logger(__name__)
_connection = None

def connect(force_renew = False):
    global _connection
    
    if not force_renew and _connection:
        return
    conn = boto.sqs.connect_to_region(
        _config.aws.region,
        aws_access_key_id = _config.aws.aws_access_key_id, 
        aws_secret_access_key = _config.aws.aws_secret_access_key
    )

    _connection = conn
    _logger.info('get connection %s', str(conn) )


def add_queue(name, timeout=_config.sqs.default_timeout):
    connect()
    q = _connection.create_queue(name, timeout)
    return q

def write_message(queue_name, message_body):
    q = get_queue(queue_name)
    m = Message()
    m.set_body(message_body)
    q.write(m)

def read_message(queue_name):
    q = get_queue(queue_name)
    rs = q.get_messages(1)
    if len(rs) == 1:
        return rs[0]
    
    return None

def read_messages(queue_name, count):
    q = get_queue(queue_name)
    rs = q.get_messages(count)
        
    return rs


def delete_message(queue_name, message):
    q = get_queue(queue_name)
    q.delete_message(message)

def get_queue(name):
    connect()
    q = _connection.get_queue(name)
    return q

def delete_queue(name):
    connect()
    q = _connection.get_queue(name)
    _connection.delete_queue(q)


def clean_all():
    connect()
    queues = _connection.get_all_queues()
    for queue in queues:
        _connection.delete_queue(queue)
    _logger.info('delete all queue' )