import inspect
import random
from abc import ABC
from dataclasses import dataclass
from types import SimpleNamespace
from typing import Literal, Callable, Any, Type, TypeVar, Generic

import pytest
from hypothesis import strategies
from loguru import logger
from punq import Container

from src.common.logging import Logger

T = TypeVar('T')

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


class LogAssertions:
    def __init__(self, container: Container):
        self.container = container
        self.logs = container.resolve(LoguruTestCapture).get_logs()

    def contains_message(self, message: str):
        self._message = message
        return self

    def with_level(self, level: str):
        self._level = level
        return self

    def with_extra(self, **extra_vars):
        self._extra_vars = extra_vars
        return self

    def exists(self):
        matching_logs = [
            log for log in self.logs
            if (hasattr(self, '_message') and self._message in log['message'])
               and (hasattr(self, '_level') and log['level'].name == self._level)
               and (not hasattr(self, '_extra_vars') or
                    all(log['extra'].get(k) == v for k, v in self._extra_vars.items()))
        ]
        assert len(matching_logs) > 0, f"No logs found matching criteria"


def assert_that_logs(container: Container):
    return LogAssertions(container)

def add_test_logging(container: Container):
    logger.remove()
    capture = LoguruTestCapture()
    logger.add(capture.capture_logs)
    container.register(LoguruTestCapture, instance=capture)
    container.register(Logger, instance=logger)


class Fixture:
    @staticmethod
    def build(cls: Type[T]) -> 'ObjectBuilder[T]':
        return ObjectBuilder(cls)

    @staticmethod
    def create(cls: Type[T]) -> T:
        return ObjectBuilder(cls).create()

    @staticmethod
    def create_many(cls: Type[T], count: int = None) -> list[T]:
        return ObjectBuilder(cls).create_many(count)

class ObjectBuilder(Generic[T]):
    def __init__(self, cls: Type[T]):
        self._cls = cls
        self._overrides = {}
        self._non_empty = True

    def with_field(self, **kwargs) -> 'ObjectBuilder[T]':
        self._overrides.update(kwargs)
        return self

    def create(self) -> T:
        if not self._overrides:
            return strategies.from_type(self._cls).example()

        return strategies.builds(
            self._cls,
            **{k: strategies.just(v) for k, v in self._overrides.items()}
        ).example()

    def create_many(self, count: int = None) -> list[T]:
        if count is None:
            count = random.Random().randint(1, 15)

        return [self.create() for _ in range(count)]



strategies.register_type_strategy(str, strategies.text(min_size=1))
strategies.register_type_strategy(float, strategies.floats(min_value=0.1))
strategies.register_type_strategy(int, strategies.integers(min_value=1))

# Force all lists to have at least 1 item - override the default min_size
original_lists = strategies.lists
strategies.lists = lambda elements, **kwargs: original_lists(elements, min_size=kwargs.get('min_size', 1), **kwargs)

fixture = Fixture()