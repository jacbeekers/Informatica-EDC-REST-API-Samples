import json

from metadata_utilities import messages


class Generic:
    """
    Some generic utilities, e.g. reading the config.json
    """
    version = "0.1.0"
    # TODO: Get the info from the file and check if that schema version exists
    metaschema_version = "0.0.0"

    def __init__(self):
        self.json_file = "resources/config.json"
        self.base_schema_folder = "unknown"
        self.version = "unknown"
        self.schema_folder = "unknown"
        self.get_config()

    def get_config(self):
        with open(self.json_file) as config:
            data = json.load(config)
            self.version = data["meta_version"]
            self.base_schema_folder = data["schema_directory"]
            self.schema_folder = self.base_schema_folder + self.version + "/"

    def main(self):
        return messages.message["ok"]["code"]


if __name__ == "__main__":
    result = Generic().main()
    print(result)
