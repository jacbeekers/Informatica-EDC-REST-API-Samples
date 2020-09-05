import logging
from metadata_utilities import generic

class MU_Logging:
    generic = generic.Generic()
    generic.get_config()

    def __init__(self):
        self.log_level_numeric =5
        self.log_level_constant = logging.DEBUG
        logger = logging.getLogger("metadata_utilities")
        self.determine_log_level(self.generic.log_level)
        logger.setLevel(self.log_level_constant)
        fh = logging.FileHandler(self.generic.log_filename)
        fh.setLevel(self.log_level_constant)
        ch = logging.StreamHandler()
        ch.setLevel(self.log_level_constant)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)

    def determine_log_level(self, log_level):
        if log_level == "DEBUG":
            self.log_level_numeric = 5
            self.log_level_constant = logging.DEBUG
#            self.log_method =

    def log(self):
