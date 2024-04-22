from ..providers import cacher, memory_cacher
from ..utils.extractor import get_cv_content


def clear_cache_control():
    '''
    Clear cache.
    '''
    cacher.reset_cache()


def extract_content_control(filedata: bytes, filename: str):
    # Save file to cache folder
    cache_file_path = memory_cacher.save_cache_file(filedata, filename)
    cv_content = get_cv_content(cache_file_path)
    memory_cacher.remove_cache_file(filename)

    return cv_content
