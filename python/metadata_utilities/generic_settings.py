import json


class GenericSettings:
    """
    Some generic utilities, e.g. reading the config.json
    """
    code_version = "0.1.0"

    def __init__(self):
        # config.json settings
        self.json_file = "resources/config.json"
        self.base_schema_folder = "unknown"
        self.meta_version = "unknown"
        self.schema_directory = "unknown"
        self.json_directory = "unknown"
        self.target = "unknown"
        self.output_directory = "unknown"
        self.metadata_store = "unknown"
        self.log_directory = "unknown"
        self.log_filename = "unknown"
        self.log_filename_prefix = "unknown"
        self.log_level = "DEBUG"
        self.get_config()

    def get_config(self):
        with open(self.json_file) as config:
            data = json.load(config)
            self.meta_version = data["meta_version"]
            self.base_schema_folder = data["schema_directory"]
            self.schema_directory = self.base_schema_folder + self.meta_version + "/"
            self.json_directory = data["json_directory"]
            self.target = data["target"]
            self.output_directory = data["output_directory"]
            self.metadata_store = data["metadata_store"]
            self.log_directory = data["log_directory"]
            self.log_filename = data["log_filename"]
            self.log_filename_prefix = data["log_filename_prefix"]
            self.log_level = data["log_level"]

