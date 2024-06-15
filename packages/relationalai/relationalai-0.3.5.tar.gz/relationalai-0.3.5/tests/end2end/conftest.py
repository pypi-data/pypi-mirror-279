import os

import pytest

from relationalai.debugging import logger
from relationalai.util.tracing_logger import TracingLogger
from tests.util import engine_config_fixture, profile_poller_fixture, root_span_fixture, snowflake_logger_fixture, span_structure_validator_fixture

# Engine is actually created in end-to-end/action.yml
# keep this in sync with that
@pytest.fixture(scope="session")
def engine_size():
    return "XS"

@pytest.fixture(scope="session")
def engine_config(engine_size):
    yield from engine_config_fixture(engine_size)

# Create a root span that all tests will be a part of
# - add `snowflake_logger` as a parameter, to make sure it is initialized before the root span
#   and finishes afterwards
# - add `span_structure_validator` as a parameter, to make sure it is initialized before the root span.
@pytest.fixture(scope="session", autouse=True)
def root_span(snowflake_logger, span_structure_validator):
    yield from root_span_fixture()

@pytest.fixture(scope="session", autouse=True)
def span_structure_validator():
    yield from span_structure_validator_fixture()

# Attach Snowflake logger; shutting down that the end of the session
@pytest.fixture(scope="session", autouse=True)
def snowflake_logger():
    yield from snowflake_logger_fixture()

@pytest.fixture(scope="session", autouse=True)
def profile_poller(engine_config):
    yield from profile_poller_fixture(engine_config)

if os.getenv('ENABLE_TRACING_LOGGER') is not None:
    logger.addHandler(TracingLogger())
