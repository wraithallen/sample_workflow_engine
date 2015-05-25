import logging


def get_logger(cls):
    """
    Generate a logger object by the given class. The logger name will be the full qualified class name.
    @param cls: A class to generate the logger.
    @type cls: C{class}
    @return: A logger by the given class.
    @rtype: U{Logger<http://docs.python.org/2/library/logging.html#logger-objects>}
    """
    if hasattr(cls, '__module__') and hasattr(cls, '__name__'):
        logger = logging.getLogger(cls.__module__ + '.' + cls.__name__)
    else:
        logger = logging.getLogger(str(cls))
    
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(levelname)s] %(message)s')
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger
