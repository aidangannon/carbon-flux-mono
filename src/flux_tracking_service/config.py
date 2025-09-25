import os
from dataclasses import dataclass

DYNAMO = "DYNAMO"

@dataclass(frozen=True, slots=True)
class DynamoSettings:
    table_name: str = os.environ.get(f"{DYNAMO}_TABLE", None)
    region: str = os.environ.get(f"{DYNAMO}_REGION", None)