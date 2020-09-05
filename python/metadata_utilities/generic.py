import glob
import json

from metadata_utilities import messages


class Generic:
    """
    Some generic utilities, e.g. reading the config.json
    """
    version = "0.1.0"
    metaschema_version = "0.0.0"

    def __init__(self):
        # config.json settings
        self.json_file = "resources/config.json"
        self.base_schema_folder = "unknown"
        self.version = "unknown"
        self.schema_directory = "unknown"
        self.json_directory = "unknown"
        self.target = "unknown"
        self.output_directory = "unknown"
        self.metadata_store = "unknown"
        self.log_directory = "unknown"
        self.log_filename = "unknown"
        self.log_filename_prefix = "unknown"
        self.log_level = "DEBUG"
        self.get_config()
        # not from config.json:
        self.attribute_list = []

    def get_config(self):
        with open(self.json_file) as config:
            data = json.load(config)
            self.version = data["meta_version"]
            self.base_schema_folder = data["schema_directory"]
            self.schema_directory = self.base_schema_folder + self.version + "/"
            self.json_directory = data["json_directory"]
            self.target = data["target"]
            self.output_directory = data["output_directory"]
            self.metadata_store = data["metadata_store"]
            self.log_directory = data["log_directory"]
            self.log_filename = data["log_filename"]
            self.log_filename_prefix = data["log_filename_prefix"]
            self.log_level = data["log_level"]

    def find_json(self, source_uuid, target_schema_type, property):
        """
        find the JSON file that has the source_uuid in the value of the property.
        The JSON schema of the file must be 'target_schema_type'.
        """
        print("target_schema_type: " + target_schema_type)
        print(f"Looking for key {property} that contains uuid {source_uuid}")
        found_meta_type = False
        found_uuid_count = 0
        directory = self.json_directory
        file_result = messages.message["not_found"]
        overall_result = messages.message["not_found"]
        # Walk through json directory and check all json files
        for file in glob.glob(directory + "*.json"):
            current_json_file = file
            print(f"\tchecking {current_json_file}")
            file_result = messages.message["not_found"]
            with open(current_json_file) as f:
                data = json.load(f)
                meta_type = data["meta"]
                meta_version = data["meta_version"]
                print(f"\t\tfile states it adheres to schema {meta_type} in version {meta_version}")
                if meta_type == target_schema_type:
                    print("\t\tcurrent metadata_type matches target_schema_type")
                    found_meta_type = True
                    try:
                        the_property_value = data[property]
                        if the_property_value == source_uuid:
                            print(f"\t\tfile contains uuid {source_uuid} in property {property}")
                            target_json_file = current_json_file
                            self.attribute_list = data["attribute_list"]
                            print(f"\t\tattribute list is: {self.attribute_list}")
                            found_uuid_count += 1
                        else:
                            print(f"\t\tfile does not contain requested uuid")
                    except KeyError as e:
                        print(f"\t\tproperty {property} and/or property 'attribute_list' do not exist in file {current_json_file}")
                        file_result = messages.message["json_key_error"]
                else:
                    print("\t\tthis is not the file we are looking for (schema_types do not match)")
                    file_result = messages.message["not_found"]

        if found_meta_type:
            print(f"found schema_type in {target_json_file}")
            if found_uuid_count == 1:
                print(f"uuid {source_uuid} has been found {found_uuid_count} time")
                overall_result = messages.message["ok"]
            elif found_uuid_count > 1:
                print(
                    f"uuid has been found {found_uuid_count} times, i.e. in multiple files of type {target_schema_type}. This is not allowed.")
                overall_result = messages.message["json_multiple_uuids_found"]
            else:
                print(f"uuid {source_uuid} could not be found")
                overall_result = messages.message["json_uuid_not_found"]
        else:
            print(f"no JSON with target_schema_type {target_schema_type}")
            overall_result = file_result

        return overall_result

    def write_local_file(self, filename, to_write):
        # local file system
        file_result = messages.message["ok"]
        path = self.output_directory + filename
        print(f"writing >{to_write}< to file >{path}<...")
        try:
            with open(path, "w") as f:
                f.write(to_write)
            print("write completed")
        except OSError as e:
            print("OS error ({0}): {1}".format(e.errno, e.strerror))
            file_result = messages.message["os_error"]
        return file_result

    def convert_list_into_string(self, list):
        print(list)
        concatenated = ""
        nr_cols = 0
        for item in list:
            # print(item)
            for attribute in ["name"]:
                # print(item[attribute])
                nr_cols += 1
                if nr_cols == 1:
                    concatenated = item[attribute]
                else:
                    concatenated += "," + item[attribute]
        return concatenated

    def main(self):
        return messages.message["not_implemented"]


if __name__ == "__main__":
    result = Generic().main()
    print(result["code"] + ": " + result["message"])
