import inspect
from abc import ABC
from dataclasses import dataclass
from typing import Literal, Callable, Any

import pytest
from loguru import logger
from punq import Container

from src.common.logging import Logger

StepName = Literal["given", "when", "then", "and"]


def scenario(func):
    return pytest.mark.test(func)


def substitute_args_into_func_display_name(func_name: str, param_values: dict[str, Any]) -> str:
    result = func_name
    for param_name, value in param_values.items():
        uppercase_param = param_name.upper()
        if uppercase_param in result:
            result = result.replace(uppercase_param, f"'{str(value)}'")

    return result


def step(func):
    def wrapper(*args, **kwargs) -> StepWrapperReturn:
        all_args = list(args) + list(kwargs.values())
        params = list(inspect.signature(func).parameters.keys())
        param_values = dict(zip(params, all_args))
        return StepWrapperReturn(
            lambda: func(*args, **kwargs),
            func.__name__,
            param_values
        )

    return wrapper


@dataclass(frozen=True, slots=True)
class StepWrapperReturn:
    func: Callable
    func_name: str
    param_values: dict[str, Any]


@dataclass(frozen=True, slots=True)
class Step:
    func: Callable
    func_name: str
    param_values: dict[str, Any]
    name: StepName

    def __str__(self):
        func_name = self.func_name.replace('_', ' ')
        display_name = substitute_args_into_func_display_name(func_name, self.param_values)
        return f"{self.name:<5}\t{display_name}"


@dataclass(frozen=True, slots=True)
class StepFailure:
    exception: Exception
    name: str


def step_expects_context(step: Step):
    params = list(inspect.signature(step.func).parameters.values())

    return len(params) > 0 and params[0].name == 'context'


class ScenarioRunner:
    steps: list[Step]
    failures: list[StepFailure]
    context: 'BaseBddContext' = None

    def __init__(self, context: 'BaseBddContext' = None):
        self.failures = []
        self.steps = []
        self.context = context

    def append_step(self,
        step: Callable,
        func_name: str,
        name: StepName,
        param_values: dict
    ) -> 'ScenarioRunner':
        self.steps.append(
            Step(
                func=step,
                func_name=func_name,
                name=name,
                param_values=param_values
            )
        )
        return self

    def given(self, step_wrapper_return: StepWrapperReturn) -> 'ScenarioRunner':
        return self.append_step(
            step_wrapper_return.func,
            step_wrapper_return.func_name,
            'given',
            step_wrapper_return.param_values,
        )

    def when(self, step_wrapper_return: StepWrapperReturn) -> 'ScenarioRunner':
        return self.append_step(
            step_wrapper_return.func,
            step_wrapper_return.func_name,
            'when',
            step_wrapper_return.param_values,
        )

    def then(self, step_wrapper_return: StepWrapperReturn) -> 'ScenarioRunner':
        return self.append_step(
            step_wrapper_return.func,
            step_wrapper_return.func_name,
            'then',
            step_wrapper_return.param_values,
        )

    def and_also(self, step_wrapper_return: StepWrapperReturn) -> 'ScenarioRunner':
        return self.append_step(
            step_wrapper_return.func,
            step_wrapper_return.func_name,
            'and',
            step_wrapper_return.param_values,
        )

    def run(self):
        print("\n")
        for step in self.steps:
            step_str = str(step)
            try:
                step.func()
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