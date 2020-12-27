from edc_rest_api.metadata_utilities import log_settings, messages
import pytest

# @pytest.mark.usefixtures("edc_config_jinja_config_is_none")


def test_get_config_is_none(capsys):
    log_settings.LogSettings(configuration_file=None)
    # assert result == messages.message["log_config_is_none"]
    captured = capsys.readouterr()
    assert "log_config is None" in captured.out


def test_get_config_does_not_exist(capsys):
    log_settings.LogSettings(configuration_file="no-no-no-no-no-no")
    # assert result == messages.message["log_config_is_none"]
    captured = capsys.readouterr()
    assert "No such file or directory" in captured.out


@pytest.mark.usefixtures("log_config_missing_log_level")
def test_log_settings_missing_log_level(capsys, log_config_missing_log_level):
    log_settings.LogSettings(configuration_file=log_config_missing_log_level)
    captured = capsys.readouterr()
    assert "Missing log_level. Set to default" in captured.out


@pytest.mark.usefixtures("log_level_verbose")
def test_log_level_verbose(capsys, log_level_verbose):
    log_settings.LogSettings(configuration_file=log_level_verbose)
    captured = capsys.readouterr()
    assert "Log level has been set to VERBOSE." in captured.out


@pytest.mark.usefixtures("log_level_debug")
def test_log_level_debug(capsys, log_level_debug):
    log_settings.LogSettings(configuration_file=log_level_debug)
    captured = capsys.readouterr()
    assert "Log level has been set to DEBUG." in captured.out


@pytest.mark.usefixtures("log_level_info")
def test_log_level_info(capsys, log_level_info):
    log_settings.LogSettings(configuration_file=log_level_info)
    captured = capsys.readouterr()
    assert "Log level has been set to INFO." in captured.out


@pytest.mark.usefixtures("log_level_warning")
def test_log_level_warning(capsys, log_level_warning):
    log_settings.LogSettings(configuration_file=log_level_warning)
    captured = capsys.readouterr()
    assert "Log level has been set to WARNING." in captured.out


@pytest.mark.usefixtures("log_level_error")
def test_log_level_error(capsys, log_level_error):
    log_settings.LogSettings(configuration_file=log_level_error)
    captured = capsys.readouterr()
    assert "Log level has been set to ERROR." in captured.out


@pytest.mark.usefixtures("log_level_fatal")
def test_log_level_fatal(capsys, log_level_fatal):
    log_settings.LogSettings(configuration_file=log_level_fatal)
    captured = capsys.readouterr()
    assert "Log level has been set to FATAL." in captured.out


@pytest.mark.usefixtures("log_level_wrong")
def test_log_level_wrong(capsys, log_level_wrong):
    log_settings.LogSettings(configuration_file=log_level_wrong)
    captured = capsys.readouterr()
    assert "invalid log level >WRONG<" in captured.out


@pytest.mark.usefixtures("log_incorrect_azure_requests")
def test_log_settings_azure_wrong(capsys, log_incorrect_azure_requests):
    log_settings.LogSettings(configuration_file=log_incorrect_azure_requests)
    captured = capsys.readouterr()
    assert "Incorrect config value >" in captured.out


@pytest.mark.usefixtures("log_azure_requests_true")
def test_log_settings_azure_true(capsys, log_azure_requests_true):
    log_settings.LogSettings(configuration_file=log_azure_requests_true)
    captured = capsys.readouterr()
    assert "azure_monitor_requests has been set to True" in captured.out


@pytest.mark.usefixtures("log_azure_requests_false")
def test_log_settings_azure_false(capsys, log_azure_requests_false):
    log_settings.LogSettings(configuration_file=log_azure_requests_false)
    captured = capsys.readouterr()
    assert "azure_monitor_requests has been set to False" in captured.out
