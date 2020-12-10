
from src.edc_utilities import edc_custom_attributes
from src.metadata_utilities import generic_settings, generic
from src.metadata_utilities import messages
from src.metadata_utilities import mu_logging


def get_settings(name="tests/resources/config.json"):
    settings = generic_settings.GenericSettings(name)
    settings.get_config()
    mu_log = mu_logging.MULogging(settings.log_config)
    generic_ref = generic.Generic(settings=settings, mu_log_ref=mu_log)
    return settings, mu_log, generic_ref


def do_not_yet_test_get_custom_attribute_exists():
    name = "dummy"
    settings, mu_log, generic_ref = get_settings()
    result = edc_custom_attributes.EDCCustomAttribute(settings).get_custom_attribute(name, expect_to_exist=True)
    assert result == messages.message["ok"]
    # test without settings_ref
    result = edc_custom_attributes.EDCCustomAttribute().get_custom_attribute(name, expect_to_exist=True)
    assert result == messages.message["ok"]
    # test with non-existent settings file
    result = edc_custom_attributes.EDCCustomAttribute(settings_ref=None
                                                      , configuration_file="does_not_exist.json").get_custom_attribute(
        name)
    assert result == messages.message["main_config_not_found"]


def test_get_custom_attribute_does_not_exists():
    name = "does_not_exist"
    settings, mu_log, generic_ref = get_settings()
    result = edc_custom_attributes.EDCCustomAttribute(settings).get_custom_attribute(name, expect_to_exist=False)
    print(result)
    assert result == messages.message["custom_attribute_not_found"]


def test_create_custom_attribute():
    name = "dummy"
    settings, mu_log, generic_ref = get_settings()
    result = edc_custom_attributes.EDCCustomAttribute(settings).create_custom_attribute()
    assert result == messages.message["no_custom_attribute_provided"]


def test_update_custom_attribute():
    name = "dummy"
    settings, mu_log, generic_ref = get_settings()
    result = edc_custom_attributes.EDCCustomAttribute(settings).update_custom_attribute(name)
    assert result == messages.message["ok"]


def test_delete_custom_attribute():
    name = "dummy"
    settings, mu_log, generic_ref = get_settings()

    # default value ignore_already_gone
    result = edc_custom_attributes.EDCCustomAttribute(settings_ref=settings).delete_custom_attribute(
        name
    )
    assert result == messages.message["ok"]

    # ignore_already_gone=True
    result = edc_custom_attributes.EDCCustomAttribute(settings_ref=settings).delete_custom_attribute(
        name
        , ignore_already_gone=True
    )
    assert result == messages.message["ok"]

    # ignore_already_gone=False
    result = edc_custom_attributes.EDCCustomAttribute(settings_ref=settings).delete_custom_attribute(
        name
        , ignore_already_gone=False
    )
    assert result == messages.message["ok"]

