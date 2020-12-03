import logging
from datetime import datetime

from opencensus.ext.azure.log_exporter import AzureLogHandler

from metadata_utilities import log_settings


class MULogging:
    code_version = "0.2.12"
    VERBOSE = 6
    DEBUG = 5
    INFO = 4
    WARNING = 3
    ERROR = 2
    FATAL = 1
    log_setting = log_settings.LogSettings()
    # log_setting.get_config()
    logger = logging.getLogger("metadata_utilities")
    logging_log_level = logging.DEBUG
    log_level = DEBUG
    right_now = datetime.now().isoformat(timespec="microseconds").replace(":","-")
    # add prefix. Allow for limited number of functions
    if log_setting.log_filename_prefix == "{{timestamp}}":
        log_path = log_setting.log_directory + right_now + "-" + log_setting.log_filename
    else:
        log_path = log_setting.log_directory + log_setting.log_filename
    fh = logging.FileHandler(log_path)
    fh.setLevel(logging_log_level)
    ch = logging.StreamHandler()
    ch.setLevel(logging_log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)
    # add azure monitor if configured
    if log_setting.instrumentation_key != "unknown" and log_setting.azure_monitor_requests == "True":
        logger.addHandler(AzureLogHandler(connection_string="InstrumentationKey=" + log_setting.instrumentation_key))

    def __init__(self):
        self.determine_log_level(self.log_setting.log_level)
        self.logger.setLevel(self.logging_log_level)
        self.area = None

    def determine_log_level(self, configured_log_level):
        if configured_log_level == "VERBOSE":
            self.log_level = self.VERBOSE
            self.logging_log_level = logging.DEBUG
        elif configured_log_level == "DEBUG":
            self.log_level = self.DEBUG
            self.logging_log_level = logging.DEBUG
        elif configured_log_level == "INFO":
            self.log_level = self.INFO
            self.logging_log_level = logging.INFO
        elif configured_log_level == "WARNING":
            self.log_level = self.WARNING
            self.logging_log_level = logging.WARNING
        elif configured_log_level == "ERROR":
            self.log_level = self.ERROR
            self.logging_log_level = logging.ERROR
        elif configured_log_level == "FATAL":
            self.log_level = self.FATAL
            self.logging_log_level = logging.FATAL
        else:
            print(f"invalid log level >{configured_log_level}< in config.json. Defaulting to DEBUG")
            self.log_level = self.DEBUG
            self.logging_log_level = logging.DEBUG

    def log(self, level=DEBUG, msg="no_message", method="undetermined", extra=None):
        if level <= self.log_level:
            if extra is None:
                properties = {"custom_dimensions": { "process": __name__, "code_version": self.code_version}}
            else:
                properties = {"custom_dimensions": extra}
            message = ""
            if self.area is None:
                message += method + " - " + msg
            else:
                message = method + " - " + self.area + " - " + msg
            if level == self.FATAL:
                self.logger.critical(message, extra=properties)
            elif level == self.ERROR:
                self.logger.error(message, extra=properties)
            elif level == self.WARNING:
                self.logger.warning(message, extra=properties)
            elif level == self.INFO:
                self.logger.info(message, extra=properties)
            elif level == self.DEBUG:
                self.logger.debug(message, extra=properties)
            else:
                self.logger.debug(message, extra=properties)
