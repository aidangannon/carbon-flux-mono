from random import randint

from tests import fixture


def create_dynamo_tracked_site(include_last_fetched = True) -> dict:
    return {
        "name": fixture.create(str),
        "last_fetched": fixture.create(int) if include_last_fetched else None,
    }

def create_dynamo_tracked_sites(include_last_fetched = True) -> list[dict]:
    return [create_dynamo_tracked_site(include_last_fetched) for _ in range(randint(1, 10))]