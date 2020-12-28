import glob
import json
import jinja2
from edc_rest_api.metadata_utilities import messages, generic_settings
import os


class Generic:
    """
    Some generic utilities, e.g. reading the config.json
    """
    code_version = "0.3.9"

    def __init__(self, settings, mu_log_ref):
        module = __name__ + ".__init__"
        self.attribute_list = []
        self.json_file = ""
        self.data = {}
        self.found_data = {}
        self.index = -1
        self.settings_found = False
        self.settings = settings
        self.mu_log = mu_log_ref
        self.mu_log.log(self.mu_log.DEBUG, "Using provided settings.", module)
        self.settings_found = True
        self.json_file = self.settings.main_config_file
        self.jinja_environment = None
        self.jinja_base_directory = None
        self.jinja_template_directory = None
        self.jinja_application = None
        self.jinja_templates = None
        self.jinja_configuration_file = self.settings.jinja_config
        self.get_jinja_settings()

    def find_json(self, source_uuid, target_schema_type, property, log_prefix="", skip_file_list=None):
        """
        find the JSON file that has the source_uuid in the value of the property.
        The JSON schema of the file must be 'target_schema_type'.
        Params:
            source_uuid: the uuid for search for
            target_schema_type: which schema. Will filter on only those files that contain the specified entity type
            property: which property (key) in the file should contain the uuid
            log_prefix: text that will be added to any log messages. Useful to identify the related log entries
        """
        module = __name__ + ".find_json"
        if not self.settings_found:
            self.mu_log.log(self.mu_log.ERROR, log_prefix + " settings were not found. Skipping processing.", module)
            return messages.message["main_config_not_found"]

        self.mu_log.log(self.mu_log.DEBUG, log_prefix + "target_schema_type: " + target_schema_type, module)
        self.mu_log.log(self.mu_log.DEBUG, log_prefix + "Looking for key >" + property + "< that contains uuid >"
                        + source_uuid + "<", module)
        found_meta_type = False
        found_uuid_count = 0
        directory = self.settings.json_directory
        self.mu_log.log(self.mu_log.DEBUG, log_prefix + "Looking in directory: " + directory, module)
        file_result = messages.message["not_found"]
        overall_result = messages.message["not_found"]
        # Walk through json directory and check all json files
        for file in glob.glob(directory + "*.json"):
            if skip_file_list is not None:
                if file in skip_file_list:
                    self.mu_log.log(self.mu_log.VERBOSE, log_prefix + "File is in exclusion list. Skipped.")
                    continue
            current_json_file = file
            self.mu_log.log(self.mu_log.DEBUG, log_prefix + "checking >" + current_json_file + "<", module)
            file_result = messages.message["not_found"]
            with open(current_json_file) as f:
                self.data = json.load(f)
                if "meta" not in self.data or "meta_version" not in self.data:
                    self.mu_log.log(self.mu_log.ERROR, log_prefix +
                                    "The keys 'meta' and 'meta_version' are required, but not found in" + current_json_file
                                    , module)
                    file_result = messages.message["meta_error"]
                    continue

                meta_type = self.data["meta"]
                meta_version = self.data["meta_version"]
                self.mu_log.log(self.mu_log.VERBOSE, log_prefix +
                                "File states it adheres to schema >" + meta_type + "<, version >"
                                + meta_version + "<", module)
                if meta_type == target_schema_type:
                    self.mu_log.log(self.mu_log.DEBUG, log_prefix + "meta_type matches", module)
                    if property in self.data:
                        self.mu_log.log(self.mu_log.DEBUG, log_prefix
                                        + "File contains property >" + property + "<", module)
                        found_meta_type = True
                        try:
                            the_property_value = self.data[property]
                            if the_property_value == source_uuid:
                                self.mu_log.log(self.mu_log.DEBUG, log_prefix +
                                                "File contains uuid >" + source_uuid + "< in property >" + property
                                                + "<", module)
                                self.json_file = current_json_file
                                self.found_data = self.data
                                found_uuid_count += 1
                                try:
                                    self.attribute_list = self.data["attribute_list"]
                                    self.mu_log.log(self.mu_log.VERBOSE, log_prefix
                                                    + "attribute list is >" + str(self.attribute_list) + "<"
                                                    , module)
                                except KeyError as e:
                                    self.attribute_list = []
                            else:
                                self.mu_log.log(self.mu_log.DEBUG, log_prefix + "file does not contain requested uuid",
                                                module)
                        except KeyError as e:
                            self.mu_log.log(self.mu_log.DEBUG, log_prefix +
                                            "property >" + property + "< does not exist in file >"
                                            + current_json_file + "<", module)
                            file_result = messages.message["json_key_error"]
                    else:
                        if "attribute_list" in self.data:
                            self.mu_log.log(self.mu_log.VERBOSE, log_prefix + "JSON file contains attribute_list",
                                            module)
                            i = -1
                            for attribute in self.data["attribute_list"]:
                                i += 1
                                self.mu_log.log(self.mu_log.VERBOSE, log_prefix
                                                + "checking uid >"
                                                + attribute["uid"]
                                                + "<", module)
                                if attribute["uid"] == source_uuid:
                                    self.mu_log.log(self.mu_log.DEBUG, log_prefix + "current uuid >" + attribute["uid"]
                                                    + "< matches source_uuid", module)
                                    found_meta_type = True
                                    found_uuid_count += 1
                                    self.found_data = self.data
                                    self.index = i
                                    break
                                # else:
                                #     self.mu_log.log(self.mu_log.VERBOSE, log_prefix
                                #                     + "This is not the UUID we are looking for", module)
                        else:
                            self.mu_log.log(self.mu_log.VERBOSE, "property and attribute_list are not in the file",
                                            module)
                else:
                    self.mu_log.log(self.mu_log.VERBOSE, log_prefix +
                                    "This is not the file we are looking for (schema_types do not match)", module)
                    file_result = messages.message["not_found"]

        if found_meta_type:
            self.mu_log.log(self.mu_log.DEBUG, log_prefix + "found schema_type in >" + self.json_file + "<", module)
            if found_uuid_count == 1:
                self.mu_log.log(self.mu_log.DEBUG, log_prefix
                                + "uuid >" + source_uuid + "< has been found " + str(found_uuid_count)
                                + " time", module)
                overall_result = messages.message["ok"]
            elif found_uuid_count > 1:
                self.mu_log.log(self.mu_log.DEBUG, log_prefix +
                                "uuid has been found " + str(found_uuid_count)
                                + " times, i.e. in multiple files of type {target_schema_type}. This is not allowed."
                                , module)
                overall_result = messages.message["json_multiple_uuids_found"]
            else:
                self.mu_log.log(self.mu_log.DEBUG, log_prefix + "uuid >" + source_uuid + "< could not be found", module)
                overall_result = messages.message["json_uuid_not_found"]
        else:
            self.mu_log.log(self.mu_log.DEBUG, log_prefix
                            + "No JSON with target_schema_type >" + target_schema_type + "<", module)
            overall_result = file_result

        return overall_result

    def write_local_file(self, directory=None, filename="dummy", to_write=""):
        # local file system
        module = __name__ + ".write_local_file"
        file_result = messages.message["ok"]
        if directory is None:
            directory = self.settings.output_directory
        path = os.path.join(directory, filename)
        os.makedirs(directory, exist_ok=True)
        self.mu_log.log(self.mu_log.DEBUG, "File name: " + path, module)
        self.mu_log.log(self.mu_log.VERBOSE, "writing >" + to_write + "< to file >" + path + "<...", module)
        try:
            with open(path, "w") as f:
                f.write(to_write)
            self.mu_log.log(self.mu_log.INFO, "File >%s< created successfully" % path, module)
        except OSError as e:
            self.mu_log.log(self.mu_log.ERROR, "OS error: " + str(e.errno) + " - " + e.strerror, module)
            file_result = messages.message["os_error"]
        return file_result

    def convert_list_into_string(self, list):
        module = __name__ + ".convert_list_into_string"
        concatenated = ""
        nr_cols = 0
        for item in list:
            # self.mu_log.log(self.mu_log.DEBUG, item, module)
            for attribute in ["name"]:
                # self.mu_log.log(self.mu_log.DEBUG, item[attribute], module)
                nr_cols += 1
                if nr_cols == 1:
                    concatenated = item[attribute]
                else:
                    concatenated += "," + item[attribute]
        return concatenated

    def get_jinja_settings(self):
        """
            Get the Jinja settings from the provided jinja configuration file: jinja_config key in main config.json
        """
        module = __name__ + ".get_jinja_settings"
        result = messages.message["ok"]
        if self.jinja_configuration_file is None:
            self.mu_log.log(self.mu_log.ERROR, "No jinja configuration file configured in main configuration",
                            module)
            return messages.message["jinja_config_file_not_found"]
        self.mu_log.log(self.mu_log.DEBUG, "Provided jinja config file: " + self.jinja_configuration_file, module)
        try:
            with open(self.jinja_configuration_file) as jinja:
                data = json.load(jinja)
                if "base_directory" in data:
                    self.jinja_base_directory = data["base_directory"]
                    self.mu_log.log(self.mu_log.INFO, "Jinja base directory taken from jinja configuration file >"
                                    + self.jinja_configuration_file
                                    + "<: "
                                    + self.jinja_base_directory, module)
                else:
                    self.mu_log.log(self.mu_log.INFO,
                                    "Jinja base directory setting not found in jinja configuration file."
                                    + " Using current directory")
                    self.jinja_base_directory = "."
                if "application" in data:
                    self.jinja_application = data["application"]
                    self.mu_log.log(self.mu_log.INFO, "Jinja application setting taken from jinja configuration file >"
                                    + self.jinja_configuration_file
                                    + "<: "
                                    + self.jinja_application, module)
                else:
                    self.mu_log.log(self.mu_log.INFO, "Jinja application setting not found. Using empty value", module)
                    self.jinja_application = None
                if "templates" in data:
                    self.jinja_templates = data["templates"]
                    self.mu_log.log(self.mu_log.INFO, "Jinja templates setting taken from jinja configuration file >"
                                    + self.jinja_configuration_file
                                    + "<: "
                                    + self.jinja_templates, module)
                else:
                    self.mu_log.log(self.mu_log.INFO, "Jinja templates setting not found. Using empty value", module)
                    self.jinja_templates = None

                self.jinja_template_directory = self.jinja_base_directory
                if self.jinja_application is not None:
                    self.jinja_template_directory += self.jinja_application
                if self.jinja_templates is not None:
                    self.jinja_template_directory += "/" + self.jinja_templates
                self.jinja_template_directory += "/" if not self.jinja_template_directory.endswith("/") else ""

                self.mu_log.log(self.mu_log.INFO, "Jinja template directory: " + self.jinja_template_directory, module)
                self.jinja_environment = jinja2.Environment(
                    loader=jinja2.FileSystemLoader(self.jinja_template_directory))
                self.jinja_environment.filters["safe"] = json.dumps

        except FileNotFoundError:
            self.mu_log.log(self.mu_log.ERROR,
                            "Could not find jinja configuration file: " + self.jinja_configuration_file
                            , module)
            return messages.message["jinja_config_file_not_found"]

        return result

    def get_jinja_template(self, template_name):
        module = __name__ + ".get_jinja_template"
        the_template = None
        if template_name is None:
            return messages.message["jinja_template_name_not_provided"], the_template

        self.mu_log.log(self.mu_log.DEBUG, "Jinja template requested: " + template_name, module)
        self.mu_log.log(self.mu_log.DEBUG, "Jinja template directory: " + self.jinja_template_directory, module)
        try:
            the_template = self.jinja_environment.get_template(template_name)
            self.mu_log.log(self.mu_log.DEBUG, "Found jinja template: " + template_name, module)
        except jinja2.exceptions.TemplateNotFound:
            self.mu_log.log(self.mu_log.ERROR, "Could not find jinja template >" + template_name
                            + "< in directory >" + self.jinja_template_directory + "<."
                            , module)
            return messages.message["jinja_template_not_found"], the_template

        return messages.message["ok"], the_template

