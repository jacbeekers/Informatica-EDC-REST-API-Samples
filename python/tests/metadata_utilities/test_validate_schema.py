import pytest

from edc_rest_api.metadata_utilities import validate_schema


def test_validate_schema_defaults():
    validate_ref = validate_schema.ValidateSchema()
    result, result_json = validate_ref.validate()
    assert result is False
    assert result_json is None


def test_validate_schema_testjson():
    validate_ref = validate_schema.ValidateSchema(
        filename="tests/resources/datalineage/input/harmo_physical_entity.json"
    )
    result, result_json = validate_ref.validate()
    assert result is False
    assert result_json is None


def test_validate_schema_correct_json_and_correct_schema():
    validate_ref = validate_schema.ValidateSchema(
        filename="tests/resources/datalineage/test_cases/to_validate_correct_physical_entity.json"
        ,schema_directory="tests/resources/schemas/interface/"
        ,schema="physical_entity"
    )
    result, result_json = validate_ref.validate()
    assert result is True
    assert result_json is not None


def test_validate_schema_incorrect_json_and_correct_schema():
    validate_ref = validate_schema.ValidateSchema(
        filename="tests/resources/datalineage/test_cases/to_validate_incorrect_physical_entity.json"
        ,schema_directory="tests/resources/schemas/interface/"
        ,schema="physical_entity"
    )
    result, result_json = validate_ref.validate()
    assert result is False
    assert result_json is None


def test_validate_schema_faulty_json_and_correct_schema():
    validate_ref = validate_schema.ValidateSchema(
        filename="tests/resources/datalineage/test_cases/to_validate_faulty_json_physical_entity.json"
        ,schema_directory="tests/resources/schemas/interface/"
        ,schema="physical_entity"
    )
    result, result_json = validate_ref.validate()
    assert result is False
    assert result_json is None


def test_validate_schema_main_empty_json_directory():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        validate_schema.main(config_file="tests/resources/datalineage/test_cases/3-empty-json-directory/config.json")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1


@pytest.mark.usefixtures("default_config")
def test_validate_schema_main_with_json_files(default_config):
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        validate_schema.main(config_file=default_config)
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_validate_schema_main_with_faulty_json_files():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        validate_schema.main(config_file="tests/resources/datalineage/test_cases/1-invalid-json/config.json")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 2


def test_validate_schema_non_existing_config():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        validate_schema.main(config_file="no-way-this-one-exists.for-sure.json")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 3
