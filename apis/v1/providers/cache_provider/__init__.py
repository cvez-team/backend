from typing import Type
import os
import importlib
import logging
from .base_provider import BaseCacheProvider


logger = logging.getLogger("uvicorn.info")

# Define Cache Provider alias
provider_name = os.environ.get('CACHE_PROVIDER', 'local')
logger.info(f"Using `{provider_name}` as cache provider")

# Import the cache provider based on the provider name
provider_module = importlib.import_module(
    f'.{provider_name}_provider', __package__)
CacheProvider: Type[BaseCacheProvider] = getattr(
    provider_module, f'{provider_name.capitalize()}CacheProvider')

# Intialized Cache Provider to avoid circular import
cacher = CacheProvider()
