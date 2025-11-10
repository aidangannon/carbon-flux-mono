import inspect
import random
import re
import traceback
import uuid
from abc import ABC
from dataclasses import dataclass
from typing import Literal, Callable, Any, Type, TypeVar, Generic

import pytest
from hypothesis import strategies
import loguru
from punq import Container

from src.common.logging import Logger

T = TypeVar('T')

StepName = Literal["given", "when", "then", "and"]
StepResult = Literal["passed", "failed", "skipped"]


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
    def wrapper(*args, **kwargs) -> StepWrapperResult:
        def get_param_values():
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            return dict(bound_args.arguments)
        func_name = func.__name__

        try:
            func(*args, **kwargs)
            return StepWrapperResult(
                func_name=func_name,
                get_param_values=get_param_values,
                result="passed"
            )
        except Exception as e:
            return StepWrapperResult(
                func_name=func_name,
                get_param_values=get_param_values,
                result="failed",
                error_message=str(e),
                error_stack_trace=traceback.format_exc()
            )

    return wrapper


@dataclass(slots=True)
class StepWrapperResult:
    result: StepResult
    func_name: str
    get_param_values: Callable[[], dict[str, Any]]
    error_message: str = None
    error_stack_trace: str = None

    def __bool__(self) -> bool:
        return self.result == "passed"


@dataclass(frozen=True, slots=True)
class Step:
    step_wrapper_result: StepWrapperResult
    name: StepName

    def __str__(self):
        func_name_with_vars = substitute_args_into_func_display_name(self.step_wrapper_result.func_name, self.step_wrapper_result.get_param_values())
        display_name = re.sub(r'_(?![^\']*\'[^\']*$)', ' ', func_name_with_vars)
        return f"{self.name:<5}\t{display_name}"


@dataclass(frozen=True, slots=True)
class StepFailure:
    error_message: str
    error_stack_trace: str
    name: str


class ScenarioRunner:
    steps: list[Step]
    failures: list[StepFailure]
    context: 'BaseBddContext' = None

    def __init__(self, context: 'BaseBddContext' = None):
        self.failures = []
        self.steps = []
        self.context = context

    def append_step(self,
        step_wrapper_result: StepWrapperResult,
        name: StepName
    ) -> 'ScenarioRunner':
        self.steps.append(
            Step(
                step_wrapper_result=step_wrapper_result,
                name=name
            )
        )
        return self

    def given(self, step_wrapper_return: StepWrapperResult) -> 'ScenarioRunner':
        return self.append_step(step_wrapper_return, 'given')

    def when(self, step_wrapper_return: StepWrapperResult) -> 'ScenarioRunner':
        return self.append_step(step_wrapper_return, 'when')

    def then(self, step_wrapper_return: StepWrapperResult) -> 'ScenarioRunner':
        return self.append_step(step_wrapper_return, 'then')

    def and_also(self, step_wrapper_return: StepWrapperResult) -> 'ScenarioRunner':
        return self.append_step(step_wrapper_return, 'and')

    def run_all_steps(self):
        print("\n")
        for step in self.steps:
            step_str = str(step)

            step_result = step.step_wrapper_result

            if step.step_wrapper_result:
                print(f"passed: \t{step_str}")
            else:
                print(f"failed: \t{step_str}")
                self.failures.append(StepFailure(
                    error_message=step_result.error_message,
                    name=step_str,
                    error_stack_trace=step_result.error_stack_trace)
                )

        if self.failures:
            msgs = [f"Step {failure.name} failed: {failure.error_message} stack track: {failure.error_stack_trace}" for failure in self.failures]
            raise AssertionError("\n".join(msgs))


class BaseBddContext(ABC):
    runner: ScenarioRunner

    def __init__(self):
        self.runner = ScenarioRunner(self)


@dataclass(frozen=True, slots=True)
class LogCapture:
    logs = []

    def capture_logs(self, message):
        record = message.record
        self.logs.append(record)

    def get_logs(self):
        return self.logs


class LogAssertions:
    def __init__(self, capture: LogCapture):
        self.logs = capture.get_logs()

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


def assert_that_logs(capture: LogCapture):
    return LogAssertions(capture)


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


strategies.register_type_strategy(str, strategies.builds(lambda: str(uuid.uuid4())))
strategies.register_type_strategy(float, strategies.floats(min_value=0.1))
strategies.register_type_strategy(int, strategies.integers(min_value=1))

original_lists = strategies.lists
strategies.lists = lambda elements, **kwargs: original_lists(elements, min_size=kwargs.get('min_size', 1), **kwargs)

auto_fixture = Fixture()