import uuid
import json
import sqs
import functools
from configutil import get_config
from logutil import get_logger

_config = get_config()
_logger = get_logger(__name__)

_queue_name = _config.workflow_engine.todo_queue_name


def initiliaze():
    add_todo_queue()

def add_todo_queue():
    global _queue_name
    sqs.add_queue(_queue_name)

def add_TaskAll(TaskAll):
    result_queue_name = str(uuid.uuid4())
    sqs.add_queue(result_queue_name, timeout=_config.workflow_engine.visibility_timeout_for_result_queue)
    tasks = TaskAll.get('tasks', [])
    for task_id, task in enumerate(tasks, start=1) :
        task['task_id'] = task_id
        task['result_queue_name'] = result_queue_name
        push_sub_task(task)

    return result_queue_name, len(tasks)

def push_sub_task(task):
    message_body = json.dumps(task)
    sqs.write_message(_queue_name, message_body)

def get_sub_task():
    message = sqs.read_message(_queue_name)
    if message:
        raw_data = message.get_body()
        task = json.loads(raw_data)
        task['callback'] = functools.partial(delete_sub_task, message)
        return task

    return None

def delete_sub_task(message):
    sqs.delete_message(_queue_name, message)
    _logger.info('delete message %s', str(message))


def push_sub_task_result(queue_name, result):
    message_body = json.dumps(result)
    sqs.write_message(queue_name, message_body)


def watch_result(queue_name, result_num):
    retry_flag = True
    result = {}
    
    while retry_flag:
        messages = sqs.read_messages(queue_name, result_num)
        for message in messages:
            raw_data = message.get_body()
            task = json.loads(raw_data)
            task_id = task.get('task_id')
            if task_id not in result:
                result[task_id] = task.get('result')
        if len(result) == result_num:
            retry_flag = False
    _logger.debug('All task result is %s', result)
    sqs.delete_queue(queue_name)
    return result
