from edc_rest_api.metadata_utilities import load_custom_attributes, messages


def test_read_defined_custom_attributes():
    ca = load_custom_attributes.LoadCustomAttributes()
    result, attributes = ca.read_defined_custom_attributes(
        "tests/resources/edc/custom_attributes/edc_defined_custom_attributes.json"
    )
    assert result == messages.message["ok"]


# does not matter
def test_read_defined_custom_attributes_wrong_config_file():
    ca = load_custom_attributes.LoadCustomAttributes(configuration_file="no")
    result, attributes = ca.read_defined_custom_attributes(
        "tests/resources/edc/custom_attributes/edc_defined_custom_attributes.json"
    )
    assert result == messages.message["ok"]


# does not matter
def test_read_defined_custom_attributes_no_file():
    ca = load_custom_attributes.LoadCustomAttributes()
    result, attributes = ca.read_defined_custom_attributes(
        "tests/no-no-no-no-attributes.json"
    )
    assert result == messages.message["custom_attribute_file_not_found"]


def test_load_custom_attributes_main_wrong_config_file():
    ca = load_custom_attributes.LoadCustomAttributes(configuration_file="no")
    result = ca.main()
    assert result == messages.message["main_config_issue"]

