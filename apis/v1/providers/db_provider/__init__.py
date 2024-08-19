from typing import Type
import os
import importlib
from .base_provider import BaseDatabaseProvider

# Define Database Provider alias
provider_name = os.environ.get('DB_PROVIDER', 'firebase')
provider_module = importlib.import_module(
    f'.{provider_name}_provider', __package__)
DatabaseProvider: Type[BaseDatabaseProvider] = getattr(
    provider_module, f'{provider_name.capitalize()}DatabaseProvider')
