from dataclasses import dataclass

from punq import Container

from src.common.logging import Logger


@dataclass(slots=True)
class Dependency:

    def __call__(self) -> str:
        return "do work"


@dataclass(frozen=True, slots=True)
class MyService:
    dep1: Dependency
    logger: Logger

    def __call__(self) -> str:
        self.logger.info("Logging from service", property="hello")
        return self.dep1()