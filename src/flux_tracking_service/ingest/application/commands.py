from dataclasses import dataclass

from src.flux_tracking_service.ingest.core import FluxFile
from src.flux_tracking_service.ingest.core import GetAllTrackedSites, GetFileUrlsForSite

@dataclass(frozen=True, slots=True)
class FetchNewFluxFilesToProcess:
    get_tracked_sites: GetAllTrackedSites
    get_files_for_site: GetFileUrlsForSite

    def __call__(self) -> list[FluxFile]:
        sites = self.get_tracked_sites()

        return list(
            FluxFile(site.name, file)
            for site in sites
            for file in self.get_files_for_site(site)
        )