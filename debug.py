import time

# local_settings = {}
local_settings = {'DEBUG': False, 'ARGS': False, 'KWARGS': False}


def timeifdebug(fn):
    def inner(*args, **kwargs):
        if local_settings['DEBUG']:
            print('starting', fn.__name__)
            t1 = time.time()
        result = fn(*args, **kwargs)
        if local_settings['DEBUG']:
            print('ending', fn.__name__, '; time:', time.time() - t1)
        return result
    return inner


def timeargsifdebug(fn):
    def inner(*args, **kwargs):
        if local_settings['DEBUG']:
            print(fn.__name__, args, kwargs)
            t1 = time.time()
        result = fn(*args, **kwargs)
        if local_settings['DEBUG']:
            print('ending', fn.__name__, '; time:', time.time() - t1)
        return result
    return inner
