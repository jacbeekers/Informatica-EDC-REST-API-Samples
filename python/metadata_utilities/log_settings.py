import json
from metadata_utilities import messages
# from metadata_utilities import mu_logging


class LogSettings:
    """
    Some generic utilities, e.g. reading the config.json
    """
    code_version = "0.2.18"

    def __init__(self, configuration_file="resources/log_config.json"):
        # log_config.json settings
        self.log_config = configuration_file
        self.log_directory = "unknown"
        self.log_filename = "unknown"
        self.log_filename_prefix = "unknown"
        self.log_level = "DEBUG"
        self.azure_monitor_config = "unknown"
        self.azure_monitor_requests = "False"
        self.instrumentation_key = "unknown"
        self.get_config()

    def get_config(self):
        module="get_config"
        result = messages.message["undetermined"]

        try:
            with open(self.log_config) as config:
                data = json.load(config)
                self.log_directory = data["log_directory"]
                self.log_filename = data["log_filename"]
                self.log_filename_prefix = data["log_filename_prefix"]
                if "log_level" in data:
                    self.log_level = data["log_level"]
                else:
                    self.log_level = "DEBUG"
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

            result = messages.message["ok"]
        except FileNotFoundError:
            print("No such file or directory: >" + self.log_config + "<.")
            result = messages.message["log_config_not_found"]

        return result
