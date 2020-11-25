import glob
import json

from metadata_utilities import generic_settings
from metadata_utilities import messages
from metadata_utilities import mu_logging


class Generic:
    """
    Some generic utilities, e.g. reading the config.json
    """
    code_version = "0.1.0"
    metaschema_version = "0.0.0"
    mu_log = mu_logging.MULogging()
    settings = generic_settings.GenericSettings()
    json_file = settings.json_file

    def __init__(self):
        self.attribute_list = []
        self.json_file = ""
        self.data = "{}"
        self.found_data = "{}"
        self.index = -1

    def find_json(self, source_uuid, target_schema_type, property, log_prefix = ""):
        """
        find the JSON file that has the source_uuid in the value of the property.
        The JSON schema of the file must be 'target_schema_type'.
        """
        module = "find_json"
        self.mu_log.log(self.mu_log.DEBUG, log_prefix + "target_schema_type: " + target_schema_type, module)
        self.mu_log.log(self.mu_log.DEBUG, log_prefix + "Looking for key >" + property + "< that contains uuid >"
                        + source_uuid + "<", module)
        found_meta_type = False
        found_uuid_count = 0
        directory = self.settings.json_directory
        file_result = messages.message["not_found"]
        overall_result = messages.message["not_found"]
        # Walk through json directory and check all json files
        for file in glob.glob(directory + "*.json"):
            current_json_file = file
            self.mu_log.log(self.mu_log.DEBUG, log_prefix + "checking >" + current_json_file + "<", module)
            file_result = messages.message["not_found"]
            with open(current_json_file) as f:
                self.data = json.load(f)
                if "meta" not in self.data or "meta_version" not in self.data:
                    self.mu_log.log(self.mu_log.ERROR, log_prefix +
                                    "the keys 'meta' and 'meta_version' are required, but not found in" + current_json_file
                                    , module)
                    file_result = messages.message["meta_error"]
                    continue

                meta_type = self.data["meta"]
                meta_version = self.data["meta_version"]
                self.mu_log.log(self.mu_log.DEBUG, log_prefix +
                                "file states it adheres to schema >" + meta_type + "<, version >"
                                + meta_version + "<", module)
                if meta_type == target_schema_type:
                    self.mu_log.log(self.mu_log.DEBUG, log_prefix + "meta_type matches", module)
                    if property in self.data:
                        self.mu_log.log(self.mu_log.DEBUG, log_prefix
                                        + "current metadata_type matches target_schema_type", module)
                        found_meta_type = True
                        try:
                            the_property_value = self.data[property]
                            if the_property_value == source_uuid:
                                self.mu_log.log(self.mu_log.DEBUG, log_prefix +
                                                "file contains uuid >" + source_uuid + "< in property >" + property
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
                            self.mu_log.log(self.mu_log.VERBOSE, log_prefix + "JSON file contains attribute_list", module)
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
                                else:
                                    self.mu_log.log(self.mu_log.VERBOSE, log_prefix
                                                    + "this is not the UUID we are looking for", module)
                        else:
                            self.mu_log.log(self.mu_log.DEBUG, "property and attribute_list are not in the file", module)
                else:
                    self.mu_log.log(self.mu_log.DEBUG, log_prefix +
                                    "this is not the file we are looking for (schema_types do not match)", module)
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
                            + "no JSON with target_schema_type >" + target_schema_type + "<", module)
            overall_result = file_result

        return overall_result

    def write_local_file(self, filename, to_write):
        # local file system
        module = "write_local_file"
        file_result = messages.message["ok"]
        path = self.settings.output_directory + filename
        self.mu_log.log(self.mu_log.VERBOSE, "writing >" + to_write + "< to file >" + path + "<...", module)
        try:
            with open(path, "w") as f:
                f.write(to_write)
            self.mu_log.log(self.mu_log.DEBUG, "write completed", module)
        except OSError as e:
            self.mu_log.log(self.mu_log.ERROR, "OS error: " + str(e.errno) + " - " + e.strerror, module)
            file_result = messages.message["os_error"]
        return file_result

    def convert_list_into_string(self, list):
        concatenated = ""
        nr_cols = 0
        for item in list:
            # self.mu_log.log(self.mu_log.DEBUG, item)
            for attribute in ["name"]:
                # self.mu_log.log(self.mu_log.DEBUG, item[attribute])
                nr_cols += 1
                if nr_cols == 1:
                    concatenated = item[attribute]
                else:
                    concatenated += "," + item[attribute]
        return concatenated
