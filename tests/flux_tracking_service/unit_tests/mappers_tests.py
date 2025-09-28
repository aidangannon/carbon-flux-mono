from datetime import datetime
from decimal import Decimal

from assertpy import assert_that

from src.flux_tracking_service.core import TrackedSite
from src.flux_tracking_service.flux_submission_detector.core import FluxSubmission
from src.flux_tracking_service.flux_submission_detector.crosscutting.mappers import map_data_tracked_site_to_core, \
    map_core_flux_submission_to_response, map_data_tracked_sites_to_core_tracked_sites, map_core_flux_submissions_to_responses
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

def test_map_core_flux_submission_to_response():
    # arrange
    flux_submission = fixture.create(FluxSubmission)

    # act
    flux_submission_response = map_core_flux_submission_to_response(flux_submission)

    # assert
    assert_that(flux_submission_response).is_not_none()
    assert_that(flux_submission_response["site"]).is_equal_to(flux_submission.site)
    assert_that(flux_submission_response["submission"]).is_equal_to(flux_submission.submission)
    assert_that(flux_submission_response["submission_time"]).is_equal_to(flux_submission.submission_time)

def test_map_core_flux_submission_to_response_when_flux_submission_is_none():
    # arrange
    flux_submission = None

    # act
    flux_submission_response = map_core_flux_submission_to_response(flux_submission)

    # assert
    assert_that(flux_submission_response).is_none()

def test_map_core_flux_submissions_to_responses():
    # arrange
    flux_submissions = fixture.create_many(FluxSubmission)
    expected_flux_submissions = [{
        "site": flux_submission.site,
        "submission": flux_submission.submission,
        "submission_time": flux_submission.submission_time
    } for flux_submission in flux_submissions]

    # act
    flux_submission_responses = map_core_flux_submissions_to_responses(flux_submissions)

    # assert
    assert_that(flux_submission_responses).is_not_none()
    assert_that(flux_submission_responses).is_equal_to(expected_flux_submissions)

def test_map_core_flux_submissions_to_responses_when_flux_submission_is_none():
    # arrange
    flux_submissions = None

    # act
    flux_submission_responses = map_core_flux_submissions_to_responses(flux_submissions)

    # assert
    assert_that(flux_submission_responses).is_none()