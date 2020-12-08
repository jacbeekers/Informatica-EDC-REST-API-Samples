from pathlib import Path
from src import run_edc_lineage
from src.edc_utilities import edc_custom_attributes
from src.metadata_utilities import messages
from src.metadata_utilities import generic_settings


def get_settings(name="resources/config.json"):
    if name is None:
        settings = generic_settings.GenericSettings()
        mu_log = settings.mu_log
    else:
        settings = generic_settings.GenericSettings(name)
        mu_log = settings.mu_log
    return settings, mu_log


def test_get_custom_attribute_exists():
    name = "dummy"
    settings, mu_log = get_settings()
    result = edc_custom_attributes.EDCCustomAttribute(settings).get_custom_attribute(name)
    assert result == messages.message["not_implemented"]
    # test without settings_ref
    result = edc_custom_attributes.EDCCustomAttribute().get_custom_attribute(name)
    assert result == messages.message["not_implemented"]
    # test with non-existent settings file
    result = edc_custom_attributes.EDCCustomAttribute(settings_ref=None
                                                      , configuration_file="does_not_exist.json").get_custom_attribute(name)
    assert result == messages.message["not_implemented"]


def test_get_custom_attribute_does_not_exists():
    name = "does_not_exist"
    settings, mu_log = get_settings()
    result = edc_custom_attributes.EDCCustomAttribute(settings).get_custom_attribute(name)
    print(result)
    assert result == messages.message["not_implemented"]


def test_create_custom_attribute():
    name = "dummy"
    settings, mu_log = get_settings()
    result = edc_custom_attributes.EDCCustomAttribute(settings).create_custom_attribute(name)
    assert result == messages.message["not_implemented"]


def test_update_custom_attribute():
    name = "dummy"
    settings, mu_log = get_settings()
    result = edc_custom_attributes.EDCCustomAttribute(settings).update_custom_attribute(name)
    assert result == messages.message["not_implemented"]


def test_delete_custom_attribute():
    name = "dummy"
    settings, mu_log = get_settings()

    # default value ignore_already_gone
    result = edc_custom_attributes.EDCCustomAttribute(settings).delete_custom_attribute(name)
    assert result == messages.message["ok"]

    # ignore_already_gone=True
    result = edc_custom_attributes.EDCCustomAttribute(settings).delete_custom_attribute(name
                                                                                        ,
                                                                                        ignore_already_gone=True)
    assert result == messages.message["ok"]

    # ignore_already_gone=False
    result = edc_custom_attributes.EDCCustomAttribute(settings).delete_custom_attribute(name
                                                                                        ,
                                                                                        ignore_already_gone=False)
    assert result == messages.message["not_implemented"]
