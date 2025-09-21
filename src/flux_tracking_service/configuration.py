import os
from dataclasses import dataclass


@dataclass(frozen=True, slots=True, unsafe_hash=True)
class IcosSettings:
    data_url: str = os.environ.get('ICOS_DATA_URL')
    meta_url: str = os.environ.get('ICOS_META_URL')