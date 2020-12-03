import logging
from datetime import datetime

from opencensus.ext.azure.log_exporter import AzureLogHandler

from metadata_utilities import log_settings


class MULogging:
    code_version = "0.2.21"
    right_now = datetime.now().isoformat(timespec="microseconds").replace(":", "-")
    VERBOSE = 6
    DEBUG = 5
    INFO = 4
    WARNING = 3
    ERROR = 2
    FATAL = 1
    fh = None
    ch = None
    already_set = False

    def __init__(self, log_configuration_file):
        if not self.already_set and self.fh is None:
            print("Setting up logger.")
            self.log_setting = log_settings.LogSettings(log_configuration_file)
            self.logger = logging.getLogger("metadata_utilities")
            self.logger.setLevel(self.log_setting.log_level)
            self.area = None
            logging_log_level = self.log_setting.DEBUG
            # add prefix. Allow for limited number of functions
            if self.log_setting.log_filename_prefix == "{{timestamp}}":
                log_path = self.log_setting.log_directory + self.right_now + "-" + self.log_setting.log_filename
            else:
                log_path = self.log_setting.log_directory + self.log_setting.log_filename
            self.fh = logging.FileHandler(log_path)
            self.fh.setLevel(logging_log_level)
            self.ch = logging.StreamHandler()
            self.ch.setLevel(logging_log_level)
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            self.fh.setFormatter(formatter)
            self.ch.setFormatter(formatter)
            # add the handlers to the logger
            self.logger.addHandler(self.fh)
            self.logger.addHandler(self.ch)
            # add azure monitor if configured
            if self.log_setting.instrumentation_key != "unknown" and self.log_setting.azure_monitor_requests == "True":
                self.logger.addHandler(AzureLogHandler(connection_string="InstrumentationKey=" + self.log_setting.instrumentation_key))
        self.already_set = True


    def log(self, level=5, msg="no_message", method="undetermined", extra=None):
        if level <= self.log_setting.log_level:
            if extra is None:
                properties = {"custom_dimensions": { "process": __name__, "code_version": self.code_version}}
            else:
                properties = {"custom_dimensions": extra}
            message = ""
            if self.area is None:
                message += method + " - " + msg
            else:
                message = method + " - " + self.area + " - " + msg
            if level == self.log_setting.FATAL:
                self.logger.critical(message, extra=properties)
            elif level == self.log_setting.ERROR:
                self.logger.error(message, extra=properties)
            elif level == self.log_setting.WARNING:
                self.logger.warning(message, extra=properties)
            elif level == self.log_setting.INFO:
                self.logger.info(message, extra=properties)
            elif level == self.log_setting.DEBUG:
                self.logger.debug(message, extra=properties)
            else:
                self.logger.debug(message, extra=properties)
