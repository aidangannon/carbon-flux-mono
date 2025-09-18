import io
import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import boto3
import requests
from icoscp import cpauth
from icoscp_core.icos import bootstrap

from src.common.logging import Logger


@dataclass(frozen=True, slots=True)
class Dependency:
    logger: Logger

    def __call__(self, item_id: str) -> Optional[dict]:
        self.logger.info("Logging from inner service")
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
        response = dynamodb.Table('flux-tracking-db').get_item(Key={
            'partition_key': 'item',
            'id': item_id
        })
        return response.get('Item', None)


@dataclass(frozen=True, slots=True)
class AnotherDependency:
    logger: Logger

    def __call__(self):
        ...


@dataclass(frozen=True, slots=True)
class MyService:
    dep1: Dependency
    dep2: AnotherDependency
    logger: Logger

    def __call__(self, item_id: str) -> Optional[dict]:
        with self.logger.contextualize(nested_prop="this is nested"):
            self.dep2()
            self.logger.info("Logging from service", property="hello")
            return self.dep1(item_id=item_id)