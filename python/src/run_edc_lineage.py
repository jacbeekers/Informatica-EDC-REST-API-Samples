from src.metadata_utilities import load_json_metadata

if __name__ == '__main__':
    result = load_json_metadata.ConvertJSONtoEDCLineage("resources/config.json").main()
    if result["code"] == "OK":
        exit(0)
    else:
        print("NOTOK:", result["code"], result["message"])
        exit(1)

