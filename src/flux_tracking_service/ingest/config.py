import os
from dataclasses import dataclass


ICOS = "ICOS"


@dataclass(frozen=True, slots=True)
class IcosSettings:
    data_url: str = os.environ[f"{ICOS}_DATA_URL"]
    meta_url: str = os.environ[f"{ICOS}_PORTAL_URL"]