from pathlib import Path
from src import run_edc_lineage
from src.metadata_utilities import messages
import os
import contextlib


def test_main_config_file(configuration_file="tests/resources/config.json"):
    assert Path(configuration_file).is_file()




def test_load_json_metadata(expected_message=messages.message["ok"]):
    result = run_edc_lineage.load_json_metadata.ConvertJSONtoEDCLineage().main()
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


def test_env_edc_url():
    with set_env(INFA_EDC_URL=u'http://somewhere'):
        test_load_json_metadata()


def test_env_edc_auth():
    with set_env(INFA_EDC_AUTH=u'"Authorization": something_here'):
        test_load_json_metadata()


def test_env_edc_ssl_pem():
    with set_env(INFA_EDC_SSL_PEM=u'some_ssl_pem'):
        test_load_json_metadata()


def test_env_edc_http_proxy():
    with set_env(HTTP_PROXY=u'http://my-proxy.org'):
        test_load_json_metadata()


def test_env_edc_https_proxy():
    with set_env(HTTPS_PROXY=u'https://my-proxy.org'):
        test_load_json_metadata()
