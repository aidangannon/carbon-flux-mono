from dataclasses import dataclass
from functools import wraps
from typing import Literal, Callable, Any

from loguru import logger
from punq import Container

from src.common.logging import Logger


class ScenarioRunner:
    def __init__(self):
        self.failures = []

    def assert_all(self):
        if self.failures:
            msgs = [f"Step {name} failed: {ex}" for name, ex in self.failures]
            raise AssertionError("\n".join(msgs))


def step(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        step_str = func.__name__.replace('_', ' ')
        print(step_str)
        try:
            result = func(self, *args, **kwargs)
            print(f"{step_str} passed")
            return result
        except AssertionError as e:
            print(f"{step_str} assert error")
            self.runner.failures.append((step_str, e))
        except Exception as e:
            print(f"{step_str} exception")
            self.runner.failures.append((step_str, e))
        return self

    return wrapper


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