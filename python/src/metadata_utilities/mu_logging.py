import logging
from datetime import datetime
from opencensus.ext.azure.log_exporter import AzureLogHandler
from src.metadata_utilities import log_settings
import os


class MULogging:
    """
        TODO: Code refactoring needed to use wrapper instead of complicated logging
    """
    code_version = "0.2.21"
    VERBOSE = 5
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    FATAL = logging.CRITICAL
    fh = None
    ch = None

    def __init__(self, log_configuration_file):
        self.log_setting = log_settings.LogSettings(log_configuration_file)
        self.area = None
        self.logger = self.setup_logger(self.log_setting.log_level
                                        , self.log_setting.log_filename_prefix
                                        , self.log_setting.log_directory
                                        , self.log_setting.log_filename
                                        , self.log_setting.instrumentation_key
                                        , self.log_setting.azure_monitor_requests
                                        )

    @staticmethod
    def setup_logger(log_level
                     , log_filename_prefix=""
                     , log_directory="log/"
                     , log_filename="some.log"
                     , instrumentation_key="unknown"
                     , azure_monitor_requests="False"
                     ):
        logger = logging.getLogger("metadata_utilities")
        if len(logger.handlers):
            return logger
        print("Setting up logger")
        logger.setLevel(log_level)
        right_now = datetime.now().isoformat(timespec="microseconds").replace(":", "-")
        # add prefix. Allow for limited number of functions
        if log_filename_prefix == "{{timestamp}}":
            log_path = log_directory + right_now + "-" + log_filename
        else:
            log_path = log_directory + log_filename
        os.makedirs(log_directory, exist_ok=True)
        fh = logging.FileHandler(log_path)
        fh.setLevel(log_level)
        ch = logging.StreamHandler()
        ch.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        # add azure monitor if configured
        if instrumentation_key != "unknown" and azure_monitor_requests == "True":
            logger.addHandler(
                AzureLogHandler(connection_string="InstrumentationKey=" + instrumentation_key))
        return logger

    def log(self, level=DEBUG, msg="no_message", method="undetermined", extra=None):
        if level >= self.log_setting.log_level:
            if extra is None:
                properties = {"custom_dimensions": {"process": __name__, "code_version": self.code_version}}
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
