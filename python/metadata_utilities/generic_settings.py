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
        self.edc_config = "unknown"
        self.edc_config_data = "{}"
        self.edc_url = "http://localhost:8888"
        self.edc_secrets = "unknown"
        self.jinja_config = "unknown"
        self.azure_monitor_config = "unknown"
        self.azure_monitor_requests = "False"
        self.instrumentation_key = "unknown"
        self.suppress_edc_call = "False"
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
            if "edc_config" in data:
                self.edc_config = data["edc_config"]
            if "edc_secrets" in data:
                self.edc_secrets = data["edc_secrets"]
            if "jinja_config" in data:
                self.jinja_config = data["jinja_config"]
            if "azure_monitor_config" in data:
                self.azure_monitor_config = data["azure_monitor_config"]
            if "azure_monitor_requests" in data:
                if data["azure_monitor_requests"] == "True":
                    self.azure_monitor_requests = True
                elif data["azure_monitor_requests"] == "False":
                    self.azure_monitor_requests = False
                else:
                    print("Incorrect config value >" + data["azure_monitor_requests"]
                          + "< for azure_monitor_requests. Must be True or False")
                    self.azure_monitor_requests = False
            if "suppress_edc_call" in data:
                if data["suppress_edc_call"] == "True":
                    self.suppress_edc_call = True
                elif data["suppress_edc_call"] == "False":
                    self.suppress_edc_call = False
                else:
                    print("Incorrect config value >" + data["suppress_edc_call"]
                          + "< for suppress_edc_call. Must be True or False. Will default to False")
                    self.suppress_edc_call = False


        if self.edc_config != "unknown":
            with open(self.edc_config) as edc:
                self.edc_config_data = json.load(edc)

        if self.edc_secrets != "unknown":
            with open(self.edc_secrets) as edc:
                data = json.load(edc)
                self.edc_url = data["edc_url"]

        if self.azure_monitor_config != "unknown":
            with open(self.azure_monitor_config) as az_monitor:
                data = json.load(az_monitor)
                if "instrumentation_key" in data:
                    self.instrumentation_key = data["instrumentation_key"]
