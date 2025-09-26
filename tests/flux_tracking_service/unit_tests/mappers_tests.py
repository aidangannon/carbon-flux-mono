from datetime import datetime

from assertpy import assert_that

from src.flux_tracking_service.ingest.crosscutting.mappers import map_data_tracked_site_to_core
from tests import fixture


def test_map_dynamo_tracked_site_to_core():
    # arrange
    dynamo_tracked_site = {
        "name": fixture.create(str),
        "last_fetched": fixture.create(int),
    }

    # act
    tracked_site = map_data_tracked_site_to_core(dynamo_tracked_site)

    # assert
    assert_that(tracked_site).is_not_none()
    assert_that(tracked_site.name).is_equal_to(dynamo_tracked_site["name"])
    assert_that(tracked_site.last_fetched).is_equal_to(dynamo_tracked_site["last_fetched"])

def test_map_dynamo_tracked_site_to_core_when_last_fetched_is_none():
    # arrange
    dynamo_tracked_site = {
        "name": fixture.create(str),
        "last_fetched": None,
    }

    # act
    tracked_site = map_data_tracked_site_to_core(dynamo_tracked_site)

    # assert
    assert_that(tracked_site).is_not_none()
    assert_that(tracked_site.name).is_equal_to(dynamo_tracked_site["name"])
    assert_that(tracked_site.last_fetched).is_none()

def test_map_dynamo_tracked_site_to_core_when_object_is_none():
    # arrange
    dynamo_tracked_site = None

    # act
    tracked_site = map_data_tracked_site_to_core(dynamo_tracked_site)

    # assert
    assert_that(tracked_site).is_none()