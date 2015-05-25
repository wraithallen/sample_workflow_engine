# Sample Workflow Engine

## Prove of Concept about simple work flow engine, based on AWS Simple Queue Service

### Setup
* Intall required library
```sh
pip install -r res/requirement.txt
```
* Edit conf/env_sample_work_flow.cfg, filled aws access key id & aws secrect access key
  - aws_access_key_id : ''
  - aws_secret_access_key : ''

### Running
* One Terminal Activate Engine
```sh
python bin/sample_workflow_engine
```
* It will add a sample task into queue
* Waiting result

* Another Terminal Activate Worker
```sh
python bin/sample_workflow_worker
```
* It will consume the task and put the result
