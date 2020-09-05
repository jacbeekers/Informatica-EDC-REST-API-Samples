import glob
import json

from metadata_utilities import messages
from metadata_utilities import mu_logging
from metadata_utilities import generic_settings


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

    def find_json(self, source_uuid, target_schema_type, property):
        """
        find the JSON file that has the source_uuid in the value of the property.
        The JSON schema of the file must be 'target_schema_type'.
        """
        module = "find_json"
        self.mu_log.log(self.mu_log.DEBUG, "target_schema_type: " + target_schema_type, module)
        self.mu_log.log(self.mu_log.DEBUG, "Looking for key >" + property + "< that contains uuid >"
            + source_uuid + "<", module)
        found_meta_type = False
        found_uuid_count = 0
        directory = self.settings.json_directory
        file_result = messages.message["not_found"]
        overall_result = messages.message["not_found"]
        # Walk through json directory and check all json files
        for file in glob.glob(directory + "*.json"):
            current_json_file = file
            self.mu_log.log(self.mu_log.DEBUG, "checking >" + current_json_file + "<", module)
            file_result = messages.message["not_found"]
            with open(current_json_file) as f:
                data = json.load(f)
                meta_type = data["meta"]
                meta_version = data["meta_version"]
                self.mu_log.log(self.mu_log.DEBUG,
                                "file states it adheres to schema " + meta_type + "<, version >"
                                + meta_version + "<", module)
                if meta_type == target_schema_type:
                    self.mu_log.log(self.mu_log.DEBUG, "current metadata_type matches target_schema_type", module)
                    found_meta_type = True
                    try:
                        the_property_value = data[property]
                        if the_property_value == source_uuid:
                            self.mu_log.log(self.mu_log.DEBUG,
                                            "file contains uuid >" + source_uuid + "< in property >" + property
                                            +"<", module)
                            target_json_file = current_json_file
                            self.attribute_list = data["attribute_list"]
                            self.mu_log.log(self.mu_log.VERBOSE, "attribute list is >" + str(self.attribute_list) + "<"
                                            ,module)
                            found_uuid_count += 1
                        else:
                            self.mu_log.log(self.mu_log.DEBUG, "file does not contain requested uuid", module)
                    except KeyError as e:
                        self.mu_log.log(self.mu_log.DEBUG,
                                        "property " + property + " and/or property 'attribute_list' do not exist in file >"
                                        + current_json_file + "<", module)
                        file_result = messages.message["json_key_error"]
                else:
                    self.mu_log.log(self.mu_log.DEBUG,
                                    "this is not the file we are looking for (schema_types do not match)", module)
                    file_result = messages.message["not_found"]

        if found_meta_type:
            self.mu_log.log(self.mu_log.DEBUG, "found schema_type in >" + target_json_file + "<", module)
            if found_uuid_count == 1:
                self.mu_log.log(self.mu_log.DEBUG, "uuid >" + source_uuid + "< has been found " + str(found_uuid_count)
                                + " time", module)
                overall_result = messages.message["ok"]
            elif found_uuid_count > 1:
                self.mu_log.log(self.mu_log.DEBUG,
                                "uuid has been found " + str(found_uuid_count)
                                + " times, i.e. in multiple files of type {target_schema_type}. This is not allowed."
                                , module)
                overall_result = messages.message["json_multiple_uuids_found"]
            else:
                self.mu_log.log(self.mu_log.DEBUG, "uuid >" + source_uuid + "< could not be found", module)
                overall_result = messages.message["json_uuid_not_found"]
        else:
            self.mu_log.log(self.mu_log.DEBUG, "no JSON with target_schema_type >" + target_schema_type + "<", module)
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
            self.mu_log.log(self.mu_log.DEBUG, "OS error: " + e.errno + " - " + e.strerror, module)
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
