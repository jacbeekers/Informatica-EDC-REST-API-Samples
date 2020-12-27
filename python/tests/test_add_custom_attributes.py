
import pytest

from edc_rest_api import add_custom_attributes


def test_main_add_custom_attributes():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        add_custom_attributes.main()
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 0


def test_main_add_custom_attributes_wrong_config():
    with pytest.raises(SystemExit) as pytest_wrapped_e:
        add_custom_attributes.main("no")
    assert pytest_wrapped_e.type == SystemExit
    assert pytest_wrapped_e.value.code == 1
