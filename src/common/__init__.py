from dataclasses import dataclass

from punq import Container


@dataclass(slots=True)
class Dependency:

    def __call__(self) -> str:
        return "do work"


@dataclass(frozen=True, slots=True)
class MyService:
    dep1: Dependency

    def __call__(self) -> str:
        return self.dep1()

def register_common(c: Container):
    c.register(MyService)
    c.register(Dependency)