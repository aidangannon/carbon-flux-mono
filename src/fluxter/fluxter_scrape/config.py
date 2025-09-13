import os
from dataclasses import dataclass


ICOS = "ICOS"


@dataclass(frozen=True, slots=True)
class IcosSettings:
    username: str = os.environ[f"{ICOS}_USERNAME"]
    password: str = os.environ[f"{ICOS}_PASSWORD"]