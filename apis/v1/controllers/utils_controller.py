from ..providers import cacher


def clear_cache_control():
    '''
    Clear cache.
    '''
    cacher.reset_cache()
