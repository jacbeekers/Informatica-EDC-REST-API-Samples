from src.metadata_utilities import load_custom_attributes, messages


def main(config_file, attribute_file):
    result = load_custom_attributes.LoadCustomAttributes(
        configuration_file=config_file
        , defined_custom_attribute_file=attribute_file
    ).main()
    if result == messages.message["ok"]:
        exit(0)
    else:
        print("NOTOK:", result["code"], result["message"])
        exit(1)


if __name__ == '__main__':
    main(
        config_file="resources/config.json"
        , attribute_file="resources/edc/custom_attributes/edc_defined_custom_attributes.json"
    )
