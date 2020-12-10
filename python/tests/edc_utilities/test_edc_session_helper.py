from src.edc_utilities import edc_session_helper
from src.metadata_utilities import generic_settings, messages

test_url = "http://localhost:7777"
auth = "Basic this-will-not-work=="
settings = generic_settings.GenericSettings()
settings.get_config()
edc_session = edc_session_helper.EDCSession(settings=settings)


def test_configure_edc():
    result = edc_session.configure_edc_session(catalog_url=test_url,
                                      catalog_auth=auth
                                      ,verify=False)
    assert result == messages.message["ok"]

    result = edc_session.configure_edc_session(catalog_url=test_url,
                                      catalog_auth=auth
                                      ,verify=None)
    assert result == messages.message["ok"]


def test_validate_edc_connection():
    result, json_result = edc_session.validate_edc_connection()
    # connection error
    assert result == 0
    assert json_result is None
