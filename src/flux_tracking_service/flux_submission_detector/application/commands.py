from dataclasses import dataclass

from src.common.logging import Logger
from src.flux_tracking_service.flux_submission_detector.core import FluxSubmission
from src.flux_tracking_service.flux_submission_detector.core import GetAllTrackedSites, GetLatestSubmissionFeed

@dataclass(frozen=True, slots=True)
class FetchNewFluxFilesToProcess:
    get_tracked_sites: GetAllTrackedSites
    get_latest_submission_feed: GetLatestSubmissionFeed
    logger: Logger

    def __call__(self) -> list[FluxSubmission]:
        sites = self.get_tracked_sites()

        if len(sites) == 0:
            return []

        submissions = self.get_latest_submission_feed()

        if len(submissions) == 0:
            self.logger.error("no submissions found")
            return []

        union_submissions = [
            (site.name, submissions[site.name])
            for site in sites
            if site.name in submissions and
               (site.last_fetched is None or
                submissions[site.name].submission_time > site.last_fetched)
        ]

        return [
            FluxSubmission(
                site=site,
                submission=submission.submission,
                submission_time=submission.submission_time
            )
            for site, submission in union_submissions
        ]