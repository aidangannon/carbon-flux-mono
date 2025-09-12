import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

import boto3
from icoscp import cpauth
from icoscp_core.icos import bootstrap

from src.common.logging import Logger


@dataclass(frozen=True, slots=True)
class Dependency:
    logger: Logger

    def __call__(self, item_id: str) -> Optional[dict]:
        self.logger.info("Logging from inner service")
        dynamodb = boto3.resource('dynamodb', region_name='eu-west-2')
        response = dynamodb.Table('fluxter-db').get_item(Key={
            'partition_key': 'item',
            'id': item_id
        })
        return response.get('Item', None)


@dataclass(frozen=True, slots=True)
class MyService:
    dep1: Dependency
    logger: Logger

    def __call__(self, item_id: str) -> Optional[dict]:
        with self.logger.contextualize(nested_prop="this is nested"):
            user_id = os.environ["ICOS_USERNAME"]
            password = os.environ["ICOS_PASSWORD"]
            meta, data = bootstrap.fromCredentials(user_id, password)
            cpauth.init_by(data.auth)
            self.logger.info("Logging some genuine tweaking stuff", meta=meta, data=data)
            self.logger.info("Logging from service", property="hello")
            return self.dep1(item_id=item_id)