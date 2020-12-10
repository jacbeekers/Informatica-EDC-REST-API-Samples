from src.metadata_utilities import load_custom_attributes, messages


def main(config_file="resources/config.json"):
    result = load_custom_attributes.LoadCustomAttributes(configuration_file=config_file).main()
    if result == messages.message["ok"]:
        exit(0)
    else:
        print("NOTOK:", result["code"], result["message"])
        exit(1)


if __name__ == '__main__':
    main()
