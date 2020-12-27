import json
from edc_rest_api.metadata_utilities import messages
# from metadata_utilities import mu_logging
import logging


class LogSettings:
    """
    Some generic utilities, e.g. reading the config.json
    """
    code_version = "0.3.35"
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
        self.configured_log_level_console = "INFO"
        self.log_level = self.DEBUG
        self.log_level_console = self.INFO
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
                if "log_level_console" in data:
                    self.configured_log_level_console = data["log_level_console"]
                else:
                    self.configured_log_level_console = "INFO"
                    print("module, Missing log_level for console. Set to default=\"INFO\"")
                self.log_level_console = self.determine_log_level(self.configured_log_level_console)
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
            return self.VERBOSE
        elif configured_log_level == logging.getLevelName(logging.DEBUG):
            return self.DEBUG
        elif configured_log_level == logging.getLevelName(logging.INFO):
            return self.INFO
        elif configured_log_level == logging.getLevelName(logging.WARNING):
            return self.WARNING
        elif configured_log_level == logging.getLevelName(logging.ERROR):
            return self.ERROR
        elif configured_log_level == logging.getLevelName(logging.FATAL):
            return self.FATAL
        else:
            print(f"invalid log level >{configured_log_level}< in config.json. Defaulting to DEBUG")
            return self.DEBUG
