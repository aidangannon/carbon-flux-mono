from dataclasses import dataclass


@dataclass(slots=True)
class Dependency:

    def __call__(self):
        print("do work")


@dataclass(frozen=True, slots=True)
class MyService:
    dep1: Dependency

    def __call__(self):
        self.dep1()