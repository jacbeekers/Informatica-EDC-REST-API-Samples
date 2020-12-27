from edc_rest_api.metadata_utilities import load_json_metadata


def main():
    result = load_json_metadata.ConvertJSONtoEDCLineage("resources/config.json").main(metafiles_only=True
                                                                                      , ignore_metafile_creation=False)
    print(result)
    result = load_json_metadata.ConvertJSONtoEDCLineage("resources/config.json").main(metafiles_only=False
                                                                                      , ignore_metafile_creation=True)
    print(result)
    if result["code"] == "OK":
        exit(0)
    else:
        print("NOTOK:", result["code"], result["message"])
        exit(1)


if __name__ == '__main__':
    main()