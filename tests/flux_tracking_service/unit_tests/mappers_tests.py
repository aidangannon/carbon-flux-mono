from datetime import datetime
from decimal import Decimal

from assertpy import assert_that

from src.flux_tracking_service.core import TrackedSite
from src.flux_tracking_service.flux_submission_detector.core import FluxFile
from src.flux_tracking_service.flux_submission_detector.crosscutting.mappers import map_data_tracked_site_to_core, \
    map_core_flux_file_to_response, map_data_tracked_sites_to_core_tracked_sites, map_core_flux_files_to_responses
from tests import fixture
from tests.flux_tracking_service.unit_tests import create_dynamo_tracked_site, create_dynamo_tracked_sites


def test_map_dynamo_tracked_site_to_core():
    # arrange
    dynamo_tracked_site = create_dynamo_tracked_site()

    # act
    tracked_site = map_data_tracked_site_to_core(dynamo_tracked_site)

    # assert
    assert_that(tracked_site).is_not_none()
    assert_that(tracked_site.name).is_equal_to(dynamo_tracked_site["name"])
    assert_that(tracked_site.last_fetched).is_equal_to(int(dynamo_tracked_site["last_fetched"]))

def test_map_dynamo_tracked_site_to_core_when_last_fetched_is_none():
    # arrange
    dynamo_tracked_site = create_dynamo_tracked_site(False)

    # act
    tracked_site = map_data_tracked_site_to_core(dynamo_tracked_site)

    # assert
    assert_that(tracked_site).is_not_none()
    assert_that(tracked_site.name).is_equal_to(dynamo_tracked_site["name"])
    assert_that(tracked_site.enabled).is_equal_to(True)
    assert_that(tracked_site.last_fetched).is_none()


def test_map_dynamo_tracked_site_to_core_when_object_is_none():
    # arrange
    dynamo_tracked_site = None

    # act
    tracked_site = map_data_tracked_site_to_core(dynamo_tracked_site)

    # assert
    assert_that(tracked_site).is_none()

def test_map_dynamo_tracked_sites_to_core_tracked_sites():
    # arrange
    dynamo_tracked_sites = create_dynamo_tracked_sites()
    expected_tracked_sites = [
        TrackedSite(
            name=dynamo_tracked_site["name"],
            last_fetched=dynamo_tracked_site["last_fetched"],
            enabled=True
        ) for dynamo_tracked_site in dynamo_tracked_sites]

    # act
    tracked_sites = map_data_tracked_sites_to_core_tracked_sites(dynamo_tracked_sites)

    # assert
    assert_that(tracked_sites).is_not_none()
    assert_that(tracked_sites).is_equal_to(expected_tracked_sites)

def test_map_dynamo_tracked_sites_to_core_tracked_site_when_last_fetched_is_none():
    # arrange
    dynamo_tracked_sites = create_dynamo_tracked_sites(False)
    expected_tracked_sites = [
        TrackedSite(
            name=dynamo_tracked_site["name"],
            last_fetched=None,
            enabled=True
        ) for dynamo_tracked_site in dynamo_tracked_sites]

    # act
    tracked_sites = map_data_tracked_sites_to_core_tracked_sites(dynamo_tracked_sites)

    # assert
    assert_that(tracked_sites).is_not_none()
    assert_that(tracked_sites).is_equal_to(expected_tracked_sites)

def test_map_dynamo_tracked_sites_to_core_tracked_sites_when_object_is_none():
    # arrange
    dynamo_tracked_sites = None

    # act
    tracked_sites = map_data_tracked_sites_to_core_tracked_sites(dynamo_tracked_sites)

    # assert
    assert_that(tracked_sites).is_none()

def test_map_core_flux_file_to_response():
    # arrange
    flux_file = fixture.create(FluxFile)

    # act
    flux_file_response = map_core_flux_file_to_response(flux_file)

    # assert
    assert_that(flux_file_response).is_not_none()
    assert_that(flux_file_response["site"]).is_equal_to(flux_file.site)
    assert_that(flux_file_response["file_url"]).is_equal_to(flux_file.file)

def test_map_core_flux_file_to_response_when_flux_file_is_none():
    # arrange
    flux_file = None

    # act
    flux_file_response = map_core_flux_file_to_response(flux_file)

    # assert
    assert_that(flux_file_response).is_none()

def test_map_core_flux_files_to_responses():
    # arrange
    flux_files = fixture.create_many(FluxFile)
    expected_flux_files = [{"site": flux_file.site, "file_url": flux_file.file} for flux_file in flux_files]

    # act
    flux_file_responses = map_core_flux_files_to_responses(flux_files)

    # assert
    assert_that(flux_file_responses).is_not_none()
    assert_that(flux_file_responses).is_equal_to(expected_flux_files)

def test_map_core_flux_files_to_responses_when_flux_file_is_none():
    # arrange
    flux_files = None

    # act
    flux_file_responses = map_core_flux_files_to_responses(flux_files)

    # assert
    assert_that(flux_file_responses).is_none()