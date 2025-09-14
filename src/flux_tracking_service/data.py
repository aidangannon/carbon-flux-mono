from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DynamoGetAllTrackedSites:

    def __call__(self):
        ...