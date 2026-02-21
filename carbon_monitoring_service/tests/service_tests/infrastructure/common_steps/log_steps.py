from pyight_bdd import step, assert_that_logs, LogCapture


@step
def there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE_and_extras_EXTRAS(
    message: str, level: str, extras: dict, capture: LogCapture
):
    assert_that_logs(capture).contains_message(message).with_level(level).with_extra(
        **extras
    ).exists()


@step
def there_should_be_a_log_with_severity_LEVEL_and_message_MESSAGE(
    message: str, level: str, capture: LogCapture
):
    assert_that_logs(capture).contains_message(message).with_level(level).exists()
