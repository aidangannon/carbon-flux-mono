import functools
import os
from dataclasses import dataclass, field

__all__ = ["lazy_dynamo_settings", "lazy_icos_settings"]

def get_from_env_var(key: str) -> str:
    return os.environ.get(key, None)


@dataclass(frozen=True, slots=True)
class DynamoSettings:
    table_name: str | None
    region: str | None

@dataclass(frozen=True, slots=True)
class IcosSettings:
    data_url: str | None


@functools.lru_cache(maxsize=1)
def lazy_dynamo_settings() -> DynamoSettings:
    return DynamoSettings(
        table_name=get_from_env_var("DYNAMO_TABLE"),
        region=get_from_env_var("DYNAMO_REGION"),
    )

@functools.lru_cache(maxsize=1)
def lazy_icos_settings() -> IcosSettings:
    return IcosSettings(
        data_url=get_from_env_var("ICOS_DATA_URL"),
    )