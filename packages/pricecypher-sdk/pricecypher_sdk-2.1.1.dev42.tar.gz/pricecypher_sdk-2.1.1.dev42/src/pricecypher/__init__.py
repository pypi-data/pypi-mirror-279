import pbr.version

from .collections import ScopeCollection, ScopeValueCollection
from .config_sections import ConfigSections
from .datasets import Datasets
from .rest import RestClient

__all__ = ['ScopeCollection', 'ScopeValueCollection', 'ConfigSections', 'Datasets', 'RestClient']

__version__ = pbr.version.VersionInfo('pricecypher_sdk').version_string()
