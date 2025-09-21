from punq import Container

from tests import step, assert_that_logs


@step
def there_should_be_an_LEVEL_log_with_message_MESSAGE(
    ctx,
    message: str,
    level: str
):
    assert_that_logs(ctx.container) \
        .contains_message(message) \
        .with_level(level) \
        .with_extra(**ctx.scoped_vars) \
        .exists()