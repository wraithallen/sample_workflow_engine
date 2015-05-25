import json
import gevent
import sqs
from subprocess import PIPE
from gevent.subprocess import Popen

from configutil import get_config
from logutil import get_logger
from to_do_queue import get_sub_task

_config = get_config()
_logger = get_logger(__name__)

def exec_command(*args, **kwargs):
    shell = kwargs.get("shell", False)
    process = Popen(args, stdout=PIPE, stderr=PIPE, close_fds=True, shell=shell)
    
    retcode = process.wait()
    output = process.stdout.read()
    unused_err = process.stderr.read()

    if retcode:
        _logger.debug("Command '%s' returned non-zero exit status %d", args, retcode)
        
    return retcode, output.strip()

def push_sub_task_result(queue_name, result):
    message_body = json.dumps(result)
    _logger.debug('write result %s into queue %s', result, queue_name)
    sqs.write_message(queue_name, message_body)

def process_task(task):
    cmd = task.get('cmd')
    queue_name = task.get('result_queue_name')
    callback = task.get('callback')
    if cmd and queue_name:
        retcode, output = exec_command(cmd, shell=True)
        response = {
            'task_id':task.get('task_id'),
            'result' : output
        }
        push_sub_task_result(queue_name, response)
        callback()

def geventHack():
        # Hacked for working normally under gevent
        gevent.sleep(0.01)

def forwardToGreenlet(task):
    def on_greenlet_exception(greenlet):
        _logger.error("execute task %s failed:%s", task, greenlet.exception)
        gevent.get_hub().parent.throw(greenlet.exception)

    g = gevent.spawn(process_task, task)
    g.link_exception(on_greenlet_exception)

def get_task_work():
    running_flag = True
    while running_flag:
        geventHack()
        task = get_sub_task()
        if task:
            _logger.debug('get task %s', task)
            forwardToGreenlet(task)
        else:
            _logger.debug('waiting for task')