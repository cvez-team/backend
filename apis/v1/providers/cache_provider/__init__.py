from typing import Type
import os
import importlib
from .base_provider import BaseCacheProvider

# Define Database Provider alias
provider_name = os.environ.get('CACHE_PROVIDER', 'redis')
provider_module = importlib.import_module(
    f'.{provider_name}_provider', __package__)
CacheProvider: Type[BaseCacheProvider] = getattr(
    provider_module, f'{provider_name.capitalize()}CacheProvider')

# Intialized Cache Provider to avoid circular import
cacher = CacheProvider()
