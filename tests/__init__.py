from dataclasses import dataclass
from functools import wraps

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
        step_name = func.__name__
        print(f"Incoming step: {step_name}")
        try:
            result = func(self, *args, **kwargs)
            print(f"Step {step_name} passed")
            return result
        except AssertionError as e:
            print(f"Step {step_name} assert error")
            self.runner.failures.append((step_name, e))
        except Exception as e:
            print(f"Step {step_name} exception")
            self.runner.failures.append((step_name, e))
        return self

    return wrapper


@dataclass(frozen=True, slots=True)
class BaseScenario:
    runner: ScenarioRunner = ScenarioRunner()

    def setup_scenario(self):
        pass

    def run(self):
        """Call this at the end of your test to check all steps passed"""
        self.runner.assert_all()


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