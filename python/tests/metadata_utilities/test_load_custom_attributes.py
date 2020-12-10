from src.metadata_utilities import load_custom_attributes


def test_read_defined_custom_attributes():
    ca = load_custom_attributes.LoadCustomAttributes()
    ca.read_defined_custom_attributes()


