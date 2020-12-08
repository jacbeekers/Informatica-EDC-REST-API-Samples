from src.metadata_utilities import messages
from src.metadata_utilities import generic_settings, mu_logging
import logging

class EDCCustomAttribute:
    """
    Class to get, add, update, delete custom attributes
    """

    def __init__(self, settings_ref=None, configuration_file=None):
        """
        Instance initialization
            settings_ref is a reference to an existing generic_settings object. If None, the settings will be collected
            from the configuration_file mentioned in the configuration_file argument
            If both settings_ref and configuration_file are set, the configuration_file argument will be ignored.
        """
        module = __name__ + ".__init__"
        self.settings = None
        self.settings_found = False
        self.mu_log = None

        if configuration_file is None:
           current_configuration_file = "resources/config.json"
        else:
            current_configuration_file = configuration_file

        if settings_ref is None:
            self.settings = generic_settings.GenericSettings(configuration_file=current_configuration_file)
            result = self.settings.get_config()
            if result != messages.message["ok"]:
                self.settings_found = False
            else:
                self.mu_log = self.settings.mu_log
                self.mu_log.log(self.mu_log.DEBUG, "Generic settings loaded.", module)
                self.settings_found = True
        else:
            self.settings = settings_ref
            self.settings_found = True
            if settings_ref.mu_log is None:
                self.mu_log = mu_logging.MULogging("resources/log_config.json")
                self.mu_log.setup_logger(logging.DEBUG)
                self.mu_log.log(self.mu_log.DEBUG, "Using provided generic settings.", module)

    def get_custom_attribute(self, name="dummy"):
        """
        Get the EDC attribute
        """
        return messages.message["not_implemented"]

    def create_custom_attribute(self, name="dummy"):
        """
        Create new custom attribute
        Will fail if attribute already exists
        """
        module = __name__ + ".create_custom_attribute"
        result = self.get_custom_attribute(name)
        if result == messages.message["ok"]:
            # attribute exists and we should not call EDC to create it
            self.mu_log.log(self.mu_log.ERROR, "Custom Attribute >" + name + "< already exists.", module)
            return messages.message["custom_attribute_already_exists"]
        else:
            self.mu_log.log(self.mu_log.INFO, "Custom Attribute >" + name + "< does not yet exist.", module)

        # TODO: Call EDC to create the custom attribute
        return messages.message["not_implemented"]

    def update_custom_attribute(self, name="dummy"):
        """
        Update a give custom attribute
        """
        module = __name__ + ".update_custom_attribute"
        result = self.get_custom_attribute(name)
        if result == messages.message["ok"]:
            # attribute exists and we can go ahead
            self.mu_log.log(self.mu_log.INFO, "Found Custom Attribute >" + name + "<.", module)
        else:
            self.mu_log.log(self.mu_log.ERROR, "Custom Attribute >" + name + "< not found.", module)
            return result

        # TODO: Call EDC to update the custom attribute
        return messages.message["not_implemented"]

    def delete_custom_attribute(self, name="dummy", ignore_already_gone=True):
        """
        Delete a give custom attribute
        """
        module = __name__ + ".delete_custom_attribute"
        result = self.get_custom_attribute(name)
        if result == messages.message["ok"]:
            # attribute exists and we can go ahead
            self.mu_log.log(self.mu_log.INFO, "Found Custom Attribute >" + name + "<.", module)
        else:
            if ignore_already_gone:
                self.mu_log.log(self.mu_log.INFO, "Custom Attribute >" + name + "< not found. "
                                + "ignore_already_gone=True, so ignoring this non-existing attribute error.", module)
                return messages.message["ok"]
            else:
                self.mu_log.log(self.mu_log.ERROR, "Custom Attribute >" + name + "< not found.")
                return result

        # TODO: Call EDC to remove the custom attribute
        return messages.message["not_implemented"]
