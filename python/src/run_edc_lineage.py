from src.metadata_utilities import load_json_metadata


def main():
    result = load_json_metadata.ConvertJSONtoEDCLineage("resources/config.json").main()
    if result["code"] == "OK":
        exit(0)
    else:
        print("NOTOK:", result["code"], result["message"])
        exit(1)


if __name__ == '__main__':
    main()