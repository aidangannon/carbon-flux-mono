from dataclasses import dataclass

from src.common.logging import Logger


@dataclass(frozen=True, slots=True)
class Dependency:
    logger: Logger

    def __call__(self) -> str:
        self.logger.info("Logging from inner service")
        return "do work"


@dataclass(frozen=True, slots=True)
class MyService:
    dep1: Dependency
    logger: Logger

    def __call__(self) -> str:
        with self.logger.contextualize(nested_prop="this is nested"):
            self.logger.info("Logging from service", property="hello")
            return self.dep1()