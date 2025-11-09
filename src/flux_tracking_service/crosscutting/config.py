import os
from dataclasses import dataclass

__all__ = ["dynamo_settings", "icos_settings"]

DYNAMO = "DYNAMO"
ICOS = "ICOS"

@dataclass(frozen=True, slots=True)
class DynamoSettings:
    table_name: str = os.environ.get(f"{DYNAMO}_TABLE", None)
    region: str = os.environ.get(f"{DYNAMO}_REGION", None)

@dataclass(frozen=True, slots=True)
class IcosSettings:
    data_url: str = os.environ.get(f"{ICOS}_DATA_URL", None)


dynamo_settings = DynamoSettings()
icos_settings = IcosSettings()