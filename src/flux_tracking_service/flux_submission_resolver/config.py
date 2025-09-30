import os
from dataclasses import dataclass


ICOS = "ICOS"

@dataclass(frozen=True, slots=True)
class IcosSettings:
    data_url: str = os.environ.get(f"{ICOS}_DATA_URL", None)