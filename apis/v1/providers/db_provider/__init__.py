from typing import Type
import os
import importlib
import logging
from .base_provider import BaseDatabaseProvider


logger = logging.getLogger("uvicorn.info")

# Define Database Provider alias
provider_name = os.environ.get('DB_PROVIDER', 'mongodb')
logger.info(f"Using `{provider_name}` as database provider")

# Import the database provider based on the provider name
provider_module = importlib.import_module(
    f'.{provider_name}_provider', __package__)
DatabaseProvider: Type[BaseDatabaseProvider] = getattr(
    provider_module, f'{provider_name.capitalize()}DatabaseProvider')
