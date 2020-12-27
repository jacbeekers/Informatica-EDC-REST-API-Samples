from pathlib import Path

import pytest

from edc_rest_api import run_edc_lineage
from edc_rest_api.metadata_utilities import load_json_metadata
from edc_rest_api.metadata_utilities import messages, generic_settings, mu_logging
import os
import contextlib
from edc_rest_api.edc_utilities import edc_lineage


@pytest.mark.usefixtures("default_config")
def test_main_config_file(default_config):
    assert Path(default_config).is_file()


def test_load_json_metadata(default_config, expected_message=messages.message["ok"]):
    result = load_json_metadata.ConvertJSONtoEDCLineage(configuration_file=default_config).main()
    assert result == expected_message
    # result = load_json_metadata.ConvertJSONtoEDCLineage("/tmp/config.json").main()


@contextlib.contextmanager
def set_env(**environ):
    old_environ = dict(os.environ)
    os.environ.update(environ)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_environ)


def test_env_edc_url(default_config):
    with set_env(INFA_EDC_URL=u'http://somewhere'):
        test_load_json_metadata(default_config)


def test_env_edc_auth(default_config):
    with set_env(INFA_EDC_AUTH=u'"Authorization": something_here'):
        test_load_json_metadata(default_config)


def test_env_edc_ssl_pem(default_config):
    with set_env(INFA_EDC_SSL_PEM=u'some_ssl_pem'):
        test_load_json_metadata(default_config)


def test_env_edc_http_proxy(default_config):
    with set_env(HTTP_PROXY=u'http://my-proxy.org'):
        test_load_json_metadata(default_config)


def test_env_edc_https_proxy(default_config):
    with set_env(HTTPS_PROXY=u'https://my-proxy.org'):
        test_load_json_metadata(default_config)


def test_main_run_edc_lineage():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        run_edc_lineage.main()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_edc_lineage_get_edc_data_references(default_config):
    settings = generic_settings.GenericSettings(default_config)
    settings.get_config()
    edc_test = edc_lineage.EDCLineage(settings=settings, mu_log_ref=settings.mu_log)
    result = edc_test.get_edc_data_references()
    assert result == messages.message["ok"]


@pytest.mark.usefixtures("config_without_meta")
def test_edc_lineage_get_edc_data_references_without_meta(config_without_meta):
    settings = generic_settings.GenericSettings(config_without_meta)
    result=settings.get_config()
    print("TEST - result settings.getconfig:", result)
    assert result == messages.message["ok"]
    print("TEST: - settings.log_config:", settings.log_config)
    mu_log = mu_logging.MULogging(log_configuration_file=settings.log_config)
    edc_test = edc_lineage.EDCLineage(settings=settings, mu_log_ref=mu_log)
    result = edc_test.get_edc_data_references()
    assert result == messages.message["ok"]


@pytest.mark.usefixtures("edc_config_incorrect_meta_version")
def test_edc_lineage_get_edc_data_references_incorrect_meta(edc_config_incorrect_meta_version):
    settings = generic_settings.GenericSettings(edc_config_incorrect_meta_version)
    result=settings.get_config()
    print("TEST - result settings.getconfig:", result)
    assert result == messages.message["ok"]
    print("TEST: - settings.log_config:", settings.log_config)
    mu_log = mu_logging.MULogging(log_configuration_file=settings.log_config)
    edc_test = edc_lineage.EDCLineage(settings=settings, mu_log_ref=mu_log)
    result = edc_test.get_edc_data_references()
    assert result == messages.message["unsupported_meta_version_edc_config"]


def test_edc_lineage_generate_lineage_wrong_output_type():
    edc_test = edc_lineage.EDCLineage(settings=None, mu_log_ref=None)
    result = edc_test.generate_lineage(output_type="wrong", metadata_type=None, data=None, generic_settings=None)
    assert result == messages.message["invalid_lineage_output_type"]


def test_edc_lineage_generate_lineage_csv_not_implemented():
    edc_test = edc_lineage.EDCLineage(settings=None, mu_log_ref=None)
    result = edc_test.generate_lineage(output_type="csv", metadata_type=None, data=None, generic_settings=None)
    assert result == messages.message["not_implemented"]


@pytest.mark.usefixtures("edc_config_jinja_config_is_none")
def test_edc_lineage_generate_lineage_jinja_is_none(edc_config_jinja_config_is_none):
    edc_test = edc_lineage.EDCLineage(settings=None, mu_log_ref=None)
    settings = generic_settings.GenericSettings(edc_config_jinja_config_is_none)
    result = edc_test.generate_lineage(output_type="json_payload", metadata_type=None, data=None, generic_settings=settings)
    assert result == messages.message["jinja_config_file_not_found"]
