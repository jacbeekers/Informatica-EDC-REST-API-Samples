from edc_rest_api.edc_utilities import edc_replication_lineage


def main():
    result = edc_replication_lineage.EDCReplicationLineage("resources/config.json").main()
    print(result)
    if result["code"] == "OK":
        exit(0)
    else:
        print("NOTOK:", result["code"], result["message"])
        exit(1)


if __name__ == '__main__':
    main()