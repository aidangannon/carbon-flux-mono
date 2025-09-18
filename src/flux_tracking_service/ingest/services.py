import io
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
        response = dynamodb.Table('flux-tracking-db').get_item(Key={
            'partition_key': 'item',
            'id': item_id
        })
        return response.get('Item', None)


@dataclass(frozen=True, slots=True)
class AnotherDependency:
    logger: Logger

    def __call__(self):
        user_id = os.environ["ICOS_USERNAME"]
        password = os.environ["ICOS_PASSWORD"]
        meta, data = bootstrap.fromCredentials(user_id, password)
        ec_data = meta.list_data_objects(
            datatype='http://meta.icos-cp.eu/resources/cpmeta/etcEddyFluxRawSeriesCsv',
            station='http://meta.icos-cp.eu/resources/stations/ES_FR-FBn',
            order_by={"prop": "timeEnd", "descending": True},
            limit=1
        )
        cpauth.init_by(data.auth)
        _, response = data.get_file_stream("https://data.icos-cp.eu/zip/KuarACMQOQSxh3lcQK1Sg27d/extractFile/FR-FBn_EC_202509120430_L05_F01.zip")
        response_data = response.read()
        s3 = boto3.client('s3')
        s3.put_object(
            Bucket=os.environ["BUCKET_NAME"],
            Key='FR-FBn_EC_202509120430_L05_F01.zip',
            Body=response_data
        )
        self.logger.info("Logging some genuine tweaking stuff", meta=meta, data=data)


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