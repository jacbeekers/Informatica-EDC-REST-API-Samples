import pytest


@pytest.fixture
def default_config():
    return "tests/resources/config.json"


@pytest.fixture
def main_config_does_not_exist():
    return "no-no-no-no-no-no.json"


@pytest.fixture
def config_without_meta():
    return "tests/resources/config_test_cases/1-without-meta/config.json"


@pytest.fixture
def edc_config_incorrect_meta_version():
    return "tests/resources/config_test_cases/2-incorrect-meta-version/config.json"


@pytest.fixture
def edc_config_jinja_config_is_none():
    return "tests/resources/config_test_cases/3-jinja-is-none/config.json"


@pytest.fixture
def log_config_missing_log_level():
    return "tests/resources/config_test_cases/4-incomplete-log-config/missing_log_level.json"


@pytest.fixture
def log_incorrect_azure_requests():
    return "tests/resources/config_test_cases/5-azure-requests-log-config/incorrect_azure_requests.json"


@pytest.fixture
def log_azure_requests_false():
    return "tests/resources/config_test_cases/5-azure-requests-log-config/azure_requests_false.json"


@pytest.fixture
def log_azure_requests_true():
    return "tests/resources/config_test_cases/5-azure-requests-log-config/azure_requests_true.json"


@pytest.fixture
def log_level_verbose():
    return "tests/resources/config_test_cases/6-log-levels/log_level_verbose.json"


@pytest.fixture
def log_level_debug():
    return "tests/resources/config_test_cases/6-log-levels/log_level_debug.json"


@pytest.fixture
def log_level_info():
    return "tests/resources/config_test_cases/6-log-levels/log_level_info.json"


@pytest.fixture
def log_level_warning():
    return "tests/resources/config_test_cases/6-log-levels/log_level_warning.json"


@pytest.fixture
def log_level_error():
    return "tests/resources/config_test_cases/6-log-levels/log_level_error.json"


@pytest.fixture
def log_level_fatal():
    return "tests/resources/config_test_cases/6-log-levels/log_level_fatal.json"


@pytest.fixture
def log_level_wrong():
    return "tests/resources/config_test_cases/6-log-levels/log_level_wrong.json"


@pytest.fixture
def config_suppress_edc_calls_false():
    return "tests/resources/config_test_cases/7-suppress-edc-calls-false/config.json"

