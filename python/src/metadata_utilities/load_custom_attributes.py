from src.metadata_utilities import generic_settings, generic
from src.edc_utilities import edc_custom_attributes
from src.metadata_utilities import messages, mu_logging
import json


class LoadCustomAttributes:
    """
    Load Custom Attributes
    """

    def __init__(self, configuration_file="resources/config.json"):
        self.init_ok = False
        self.config = configuration_file
        self.settings = generic_settings.GenericSettings(configuration_file)
        self.config_result = self.settings.get_config()
        self.edc_custom_attributes = edc_custom_attributes.EDCCustomAttribute()

        self.mu_log = None
        self.generic = None
        self.json_directory = None
        self.target = None
        if self.config_result == messages.message["ok"]:
            self.mu_log = mu_logging.MULogging(self.settings.log_config)
            self.generic = generic.Generic(settings=self.settings, mu_log_ref=self.mu_log)
            self.json_directory = self.settings.json_directory
            self.target = self.settings.target
            self.init_ok = True
        else:
            print("FATAL:", "settings.get_config returned:",
                  self.config_result["code"] + " - " + self.config_result["message"])
            raise EnvironmentError

    def main(self):
        module = __name__ + ".main"
        result, defined_custom_attributes = self.read_defined_custom_attributes()
        overall_result = messages.message["ok"]

        nr_custom_attributes = 0
        for defined_custom_attribute in defined_custom_attributes:
            nr_custom_attributes += 1
            self.mu_log.log(self.mu_log.DEBUG, "Custom Attribute #" + str(nr_custom_attributes), module)
            name = defined_custom_attribute["items"][0]["name"]
            # Takes too long to retrieve all attributes.
            # Just create the new one and if it already exists, seize the exception
            # result = self.edc_custom_attributes.get_custom_attribute(name)
            # if result == messages.message["ok"]:
            #    # attribute already exists
            #    self.mu_log.log(self.mu_log.ERROR, "Custom Attribute >" + name + "< already exists."
            #                    , module)
            #    overall_result = messages.message["custom_attribute_already_exists"]
            # elif result == messages.message["custom_attribute_not_found"]:
            self.mu_log.log(self.mu_log.DEBUG, "Will create new Custom Attribute >"
                            + name
                            + "<.", module)
            result = self.edc_custom_attributes.create_custom_attribute(
                custom_attribute_values=defined_custom_attribute
            )
            if result != messages.message["ok"]:
                overall_result = result

        return overall_result

    def read_defined_custom_attributes(self):
        result = messages.message["ok"]
        defined_custom_attributes = []
        try:
            with open("resources/edc/custom_attributes/edc_defined_custom_attributes.json") as attributes:
                data = json.load(attributes)
                if "defined_custom_attributes" in data:
                    defined_custom_attributes = data["defined_custom_attributes"]
        except FileNotFoundError:
            self.mu_log.log(self.mu_log.ERROR, "defined custom attribute file could not be found.")
            result = messages.message["file_not_found"]

        return result, defined_custom_attributes