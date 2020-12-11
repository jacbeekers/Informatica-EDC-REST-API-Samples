import json
from src.metadata_utilities import messages
# from metadata_utilities import mu_logging
import logging


class LogSettings:
    """
    Some generic utilities, e.g. reading the config.json
    """
    code_version = "0.2.21"
    VERBOSE = 5
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    FATAL = logging.CRITICAL

    def __init__(self, configuration_file="resources/log_config.json"):
        # log_config.json settings
        self.log_config = configuration_file
        self.log_directory = None
        self.log_filename = None
        self.log_filename_prefix = None
        self.configured_log_level = "DEBUG"
        self.log_level = self.DEBUG
        self.azure_monitor_config = None
        self.azure_monitor_requests = False
        self.instrumentation_key = None
        self.get_config()

    def get_config(self):
        module=__name__ + ".get_config"
        result = messages.message["undetermined"]

        try:
            if self.log_config is None:
                print(module, "log_config is None, i.e. an empty value was provided for the log configuration file.")
                return messages.message["log_config_is_none"]

            with open(self.log_config) as config:
                data = json.load(config)
                self.log_directory = data["log_directory"]
                self.log_filename = data["log_filename"]
                self.log_filename_prefix = data["log_filename_prefix"]
                if "log_level" in data:
                    self.configured_log_level = data["log_level"]
                else:
                    self.configured_log_level = "DEBUG"
                    print("module, Missing log_level. Set to default=\"DEBUG\"")
                self.log_level = self.determine_log_level(self.configured_log_level)
                if "azure_monitor_config" in data:
                    self.azure_monitor_config = data["azure_monitor_config"]
                if "azure_monitor_requests" in data:
                    if data["azure_monitor_requests"] == "True":
                        self.azure_monitor_requests = True
                        print(module, "azure_monitor_requests has been set to True")
                    elif data["azure_monitor_requests"] == "False":
                        self.azure_monitor_requests = False
                        print(module, "azure_monitor_requests has been set to False")
                    else:
                        print(module, "Incorrect config value >" + data["azure_monitor_requests"]
                              + "< for azure_monitor_requests. Must be True or False")
                        self.azure_monitor_requests = False
                else:
                    print(module, "azure_monitor_requests not found. Not logging to Azure.")

            result = messages.message["ok"]
        except FileNotFoundError:
            print(module, "No such file or directory: >" + self.log_config + "<.")
            result = messages.message["log_config_not_found"]

        return result

    def determine_log_level(self, configured_log_level):
        module = __name__ + ".determine_log_level"
        if configured_log_level == "VERBOSE":
            self.log_level = self.VERBOSE
            print(module, "Log level has been set to VERBOSE.")
            return self.log_level
        elif configured_log_level == logging.getLevelName(logging.DEBUG):
            self.log_level = self.DEBUG
            print(module, "Log level has been set to DEBUG.")
            return self.log_level
        elif configured_log_level == logging.getLevelName(logging.INFO):
            self.log_level = self.INFO
            print(module, "Log level has been set to INFO.")
            return self.log_level
        elif configured_log_level == logging.getLevelName(logging.WARNING):
            self.log_level = self.WARNING
            print(module, "Log level has been set to WARNING.")
            return self.log_level
        elif configured_log_level == logging.getLevelName(logging.ERROR):
            self.log_level = self.ERROR
            print(module, "Log level has been set to ERROR.")
            return self.log_level
        elif configured_log_level == logging.getLevelName(logging.FATAL):
            self.log_level = self.FATAL
            print(module, "Log level has been set to FATAL.")
            return self.log_level
        else:
            print(f"invalid log level >{configured_log_level}< in config.json. Defaulting to DEBUG")
            self.log_level = self.DEBUG
            return self.log_level
