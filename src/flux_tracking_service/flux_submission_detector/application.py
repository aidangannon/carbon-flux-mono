from dataclasses import dataclass

from src.common.logging import Logger
from src.flux_tracking_service.flux_submission_detector.core import GetAllTrackedSites, GetLatestSubmissionFeed, \
    FluxSubmission
