from src.metadata_utilities import load_custom_attributes

if __name__ == '__main__':
    result = load_custom_attributes.LoadCustomAttributes("resources/config.json").main()
    if result["code"] == "OK":
        exit(0)
    else:
        print("NOTOK:", result["code"], result["message"])
        exit(1)

