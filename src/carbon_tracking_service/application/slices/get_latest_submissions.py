from src.common import logging
from src.carbon_tracking_service.application import ports
from src.carbon_tracking_service.core import SiteSubmission


def execute(
    submission_client: ports.FluxClient,
    tracked_site_repo: ports.TrackedSiteRepository
) -> list[SiteSubmission]:
    sites = tracked_site_repo.get_all()

    if len(sites) == 0:
        return []

    submissions = submission_client.get_all_latest()

    if len(submissions) == 0:
        logging.logger.error("no submissions found")
        return []

    union_submissions = [
        (site.name, submissions[site.name])
        for site in sites
        if site.name in submissions and
           (site.last_fetched is None or
            submissions[site.name].submission_time > site.last_fetched)
    ]

    return [
        SiteSubmission(
            site=site,
            submission=submission.submission,
            submission_time=submission.submission_time
        )
        for site, submission in union_submissions
    ]