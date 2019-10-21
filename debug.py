import time

# local_settings = {}
local_settings = {'debug': False}


def timeifdebug(fn):
  def inner(*args, **kwargs):
    if local_settings['DEBUG']:
      print(fn.__name__, args, kwargs)
      t1 = time.time()
    result = fn(*args, **kwargs)
    if local_settings['DEBUG']:
      print(time.time() - t1)
    return result
  return inner
