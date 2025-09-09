from abc import ABC
from dataclasses import dataclass
from functools import wraps
from typing import Literal, Callable, Any

from loguru import logger
from punq import Container

from src.common.logging import Logger


StepName = Literal["given", "when", "then", "and\t"]


@dataclass(frozen=True, slots=True)
class Step:
    func: Callable
    name: StepName

    def __str__(self):
        return f"{self.name}\t{self.func.__name__.replace('_', ' ')}"


@dataclass(frozen=True, slots=True)
class StepFailure:
    exception: Exception
    name: str


class ScenarioRunner:
    steps: list[Step]
    failures: list[StepFailure]
    context: 'BaseBddContext' = None

    def __init__(self, context: 'BaseBddContext' = None):
        self.failures = []
        self.steps = []
        self.context = context

    def given(self, step: Callable) -> 'ScenarioRunner':
        self.steps.append(Step(func=step, name="given"))
        return self

    def when(self, step: Callable) -> 'ScenarioRunner':
        self.steps.append(Step(func=step, name="when"))
        return self

    def then(self, step: Callable) -> 'ScenarioRunner':
        self.steps.append(Step(func=step, name="then"))
        return self

    def and_also(self, step: Callable) -> 'ScenarioRunner':
        self.steps.append(Step(func=step, name="and\t"))
        return self

    def run(self):
        print("\n")
        for step in self.steps:
            step_str = str(step)
            try:
                if self.context is not None:
                    step.func(self.context)
                print(f"passed: \t{step_str}")
            except Exception as e:
                print(f"failed: \t{step_str}")
                self.failures.append(StepFailure(exception=e, name=step_str))

        if self.failures:
            msgs = [f"Step {failure.name} failed: {failure.exception}" for failure in self.failures]
            raise AssertionError("\n".join(msgs))


class BaseBddContext(ABC):
    runner: ScenarioRunner

    def __init__(self):
        self.runner = ScenarioRunner(self)


@dataclass(frozen=True, slots=True)
class LoguruTestCapture:
    logs = []

    def capture_logs(self, message):
        record = message.record
        self.logs.append(record)

    def get_logs(self):
        return self.logs

def assert_that_there_is_a_log_with(container: Container,
    message: str,
    level: str,
    **extra_vars: dict
):
    logs = container \
        .resolve(LoguruTestCapture) \
        .get_logs()
    matching_logs = [
        log for log in logs
        if message in log['message']
           and log['level'].name == level
           and all(log['extra'].get(k) == v for k, v in extra_vars.items())
    ]
    return len(matching_logs) > 0

def add_test_logging(container: Container):
    logger.remove()
    capture = LoguruTestCapture()
    logger.add(capture.capture_logs)
    container.register(LoguruTestCapture, instance=capture)
    container.register(Logger, instance=logger)