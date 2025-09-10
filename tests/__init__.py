from abc import ABC
from dataclasses import dataclass, field
from functools import wraps
from typing import Literal, Callable, Any, Optional
import inspect
import re

from loguru import logger
from punq import Container

from src.common.logging import Logger


StepName = Literal["given", "when", "then", "and"]


def substitute_args_into_func_display_name(func_name: str, step: 'Step') -> str:
    params = list(inspect.signature(step.func).parameters.keys())
    
    param_offset = 1 if params and params[0] == 'context' else 0

    if step.args:
        for i, arg in enumerate(step.args):
            param_index = i + param_offset
            if param_index < len(params):
                func_name = re.sub(params[param_index].upper(), f'"{arg}"', func_name)
    
    if step.kwargs:
        for key, value in step.kwargs.items():
            func_name = re.sub(key.upper(), f'"{value}"', func_name)
    
    return func_name


@dataclass(frozen=True, slots=True)
class Step:
    func: Callable
    name: StepName
    args: Optional[tuple[Any, ...]]
    kwargs: Optional[dict[str, Any]]

    def __str__(self):
        func_name = substitute_args_into_func_display_name(self.func.__name__, self).replace('_', ' ')
        return f"{self.name:<5}\t{func_name}"


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
        name: StepName,
        *args,
        **kwargs
    ) -> 'ScenarioRunner':
        self.steps.append(
            Step(
                func=step,
                name=name,
                args=args,
                kwargs=kwargs
            )
        )
        return self

    def given(self, step: Callable) -> 'ScenarioRunner':
        return self.append_step(step, 'given')

    def when(self, step: Callable) -> 'ScenarioRunner':
        return self.append_step(step, 'when')

    def then(self, step: Callable) -> 'ScenarioRunner':
        return self.append_step(step, 'then')

    def and_also(self, step: Callable) -> 'ScenarioRunner':
        return self.append_step(step, 'and')

    def given_with_params(self, step: Callable, *args, **kwargs) -> 'ScenarioRunner':
        return self.append_step(step, 'given', *args, **kwargs)

    def when_with_params(self, step: Callable, *args, **kwargs) -> 'ScenarioRunner':
        return self.append_step(step, 'when', *args, **kwargs)

    def then_with_params(self, step: Callable, *args, **kwargs) -> 'ScenarioRunner':
        return self.append_step(step, 'then', *args, **kwargs)

    def and_also_with_params(self, step: Callable, *args, **kwargs) -> 'ScenarioRunner':
        return self.append_step(step, 'and', *args, **kwargs)

    def call_step(self, step: Step):
        args = []
        if step_expects_context(step) and self.context is not None:
            args.append(self.context)
        
        if step.args:
            args.extend(step.args)
            
        kwargs = step.kwargs or {}
        
        step.func(*args, **kwargs)

    def run(self):
        print("\n")
        for step in self.steps:
            step_str = str(step)
            try:
                self.call_step(step)
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