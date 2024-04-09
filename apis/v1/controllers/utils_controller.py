from ..providers import cacher
from ..schemas.user_schema import UserSchema


def clear_cache_control(user: UserSchema):
    '''
    Clear cache.
    '''
    cacher.reset_cache()
