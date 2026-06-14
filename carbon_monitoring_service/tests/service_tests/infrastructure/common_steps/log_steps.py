from pyight_bdd import step, assert_that_logs, LogCapture


@step
def should_have_log_LEVEL_MESSAGE_EXTRAS(
    message: str,
    level: str,
    extras: dict,
    capture: LogCapture
):
    assert_that_logs(capture) \
        .contains_message(message) \
        .with_level(level) \
        .with_extra(**extras) \
        .exists()


@step
def should_have_log_LEVEL_MESSAGE(
    message: str,
    level: str,
    capture: LogCapture
):
    assert_that_logs(capture) \
        .contains_message(message) \
        .with_level(level) \
        .exists()
