import functools
import os
from dataclasses import dataclass

__all__ = ["lazy_dynamo_settings", "lazy_icos_settings"]

DYNAMO = "DYNAMO"
ICOS = "ICOS"

@dataclass(frozen=True, slots=True)
class DynamoSettings:
    table_name: str = os.environ.get(f"{DYNAMO}_TABLE", None)
    region: str = os.environ.get(f"{DYNAMO}_REGION", None)

@dataclass(frozen=True, slots=True)
class IcosSettings:
    data_url: str = os.environ.get(f"{ICOS}_DATA_URL", None)


@functools.lru_cache(maxsize=1)
def lazy_dynamo_settings() -> DynamoSettings:
    return DynamoSettings()

@functools.lru_cache(maxsize=1)
def lazy_icos_settings() -> IcosSettings:
    return IcosSettings()