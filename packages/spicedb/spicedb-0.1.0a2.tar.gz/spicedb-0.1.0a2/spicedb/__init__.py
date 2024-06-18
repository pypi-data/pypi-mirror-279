from importlib import metadata

from spicedb.spicedb import SpiceDB
from spicedb.types import SpiceRelationship

__version__ = metadata.version("spicedb")

__all__ = ("__version__", "SpiceDB", "SpiceRelationship")
