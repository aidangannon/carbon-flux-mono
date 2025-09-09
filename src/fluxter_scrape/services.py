from dataclasses import dataclass
from typing import Optional

import boto3

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
            self.logger.info("Logging from service", property="hello")
            return self.dep1(item_id=item_id)