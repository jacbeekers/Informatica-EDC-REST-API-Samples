import json

import jsonschema

from metadata_utilities import messages, generic


class CheckSchema:
    """
    Checks the JSON schema of a given JSON file
    """
    version = "0.1.0"
    # TODO: Get the info from the file and check if that schema version exists
    metaschema_version = generic.Generic().version
    print(f"expected meta_version is {metaschema_version}")

    def __init__(self):
        self.json_file = "not provided"
        self.meta_type = "unknown"
        self.meta_version = "unknown"
        self.schema_file = "unknown"

    def check_schema(self, json_file):
        self.json_file = json_file
        """
        Checks the JSON to determine which JSON schema is used and which version
        """

        with open(self.json_file) as f:
            data = json.load(f)
            try:
                self.meta_type = data["meta"]
                self.meta_version = data["meta_version"]
                print(f"schema of file {json_file}: {self.meta_type} in version {self.meta_version}")
            except KeyError as e:
                print("Key error. meta and meta_version must be in JSON file. That is not the case with "
                      + self.json_file)
                return messages.message["meta_error"]["code"]
            except jsonschema.exceptions.SchemaError as e:
                print("Schema error: ", e.message)
                return messages.message["json_schema_error"]["code"]
            except jsonschema.exceptions.ValidationError as e:
                print("Validation error: ", e.message)
                return messages.message["json_validation_error"]["code"]
            except json.decoder.JSONDecodeError as e:
                print("Error parsing JSON:", e.msg)
                return messages.message["json_parse_error"]["code"]
        if self.meta_version == generic.Generic().version:
            print("file meta version matches expected schema version")
            schema_directory = generic.Generic().schema_directory
            self.schema_file = schema_directory + self.meta_type + ".json"
            with open(self.schema_file) as f:
                schema = json.load(f)
                try:
                    jsonschema.validate(data, schema)
                    print("JSON file validated successfully against schema")
                except jsonschema.exceptions.SchemaError as e:
                    print("A schema error occurred during validation")
                    return messages.message["jsonschema_validation_error"]["code"]
                except jsonschema.exceptions.ValidationError as e:
                    print("A validation error occurred")
                    return messages.message["jsonschema_validation_error"]["code"]
        else:
            print("File meta version does not match expected schema version")
            return messages.message["incorrect_meta_version"]["code"]

        return messages.message["ok"]["code"]


def main(self):
    directory = "resources/Datalineage and metadata/JSON files/"
    file_name = "acq_physical_entity.json"
    return self.check_schema(directory + file_name)


if __name__ == "__main__":
    result = CheckSchema().main()
    print(result)
