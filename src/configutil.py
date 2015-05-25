import os
import re
import sys
from config import Config, ConfigMerger, defaultMergeResolve
from logutil import get_logger


_CONFIG = Config()
_logger = get_logger(__name__)

def overwriteMergeResolve(map1, map2, key):
    rv = defaultMergeResolve(map1, map2, key)
    if rv == "mismatch" or rv == "append":
        rv = "overwrite"
    return rv

def initialize(pattern = "^env.*\.cfg$"):
    global _CONFIG
    _merger = ConfigMerger(overwriteMergeResolve)
    conf_list = []
    m = re.compile(pattern)

    for path in sys.path:
        for root, directories, files in os.walk(path):
            for file_name in files:
                if not m.match(file_name):
                    continue
                
                conf_list.append(os.path.join(root, file_name))
    
    for file_path in conf_list:
        f = file(file_path)
        
        try:
            cfg = Config(f)
            _merger.merge(_CONFIG, cfg)
        except:
            _logger.warn('load config file %s failed.', file_path, exc_info = True)
        
    _logger.debug('all configurations: %s', _CONFIG)
    
def get_config():
    return _CONFIG
