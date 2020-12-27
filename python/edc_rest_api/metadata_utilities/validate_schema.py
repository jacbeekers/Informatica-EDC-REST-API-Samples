import glob
import json
import os

import jsonschema
from edc_rest_api.metadata_utilities import generic_settings, generic
from edc_rest_api.metadata_utilities import messages


class ValidateSchema():
    default_version = "0.2.0"
    default_schema_directory = "metadata/schemas/interface/"
    default_schema = "physical_entity"
    default_resource_directory = "metadata/resources/"
    default_filename = "default.json"

    def __init__(self
                 , schema_directory=default_schema_directory
                 , schema=default_schema
                 , version=default_version
                 , resource_directory=default_resource_directory
                 , filename=default_filename):
        self.version = version
        self.schema_directory = schema_directory
        self.schema = schema + ".json"
        self.against_schema = self.schema_directory + self.version + "/" + self.schema
        self.resource_directory = resource_directory + "/"
        self.filename = filename
        self.verify_file = self.filename
        # self.verify_file = self.resource_directory + self.filename

    def validate(self):

        try:
            with open(self.verify_file) as file:
                name = os.path.basename(file.name)
                print(f"Verifying {name}")
                the_doc = json.load(file)
                try:
                    with open(self.against_schema) as structure:
                        struct = os.path.basename(structure.name)
                        print(f"\t\t against {structure.name}")
                        try:
                            the_schema = json.load(structure)
                            jsonschema.validate(the_doc, the_schema)
                            return True, self.schema
                        except jsonschema.exceptions.ValidationError as e:
                            print(f"\t\t Validation error:{e.message} ")
                        except json.decoder.JSONDecodeError as e:
                            print(f"\t\t ERROR parsing JSON:{e.msg} line {e.lineno} col {e.colno}")
                except FileNotFoundError:
                    print(f"\t\t Schema file not found: " + self.against_schema)

        except FileNotFoundError:
            print(f"\t\t File to be validated not found: " + self.verify_file)

        return False, None


def main(config_file="resources/config.json"):
    json_file = "not provided"
    meta_type = "unknown"
    result = messages.message["undetermined"]
    settings = generic_settings.GenericSettings(configuration_file=config_file)
    result = settings.get_config()
    if result != messages.message["ok"]:
        print("ERROR:", result["message"])
        exit(3)

    json_directory = settings.json_directory
    target = settings.target
    data = ""

    number_of_files = 0
    number_of_errors = 0

    # json_directory = "resources/datalineage/input/"
    print("JSON directory is: " + json_directory)

    for file in glob.glob(json_directory + "*.json"):
        number_of_files += 1
        with open(file) as f:
            the_schema = json.load(f)
            try:
                meta_type = the_schema["meta"]
                meta_version = the_schema["meta_version"]
                print("schema is " + meta_type + " version " + meta_version)
            except KeyError as e:
                print("Key error. meta and meta_version must be in JSON file. That is not the case with " + file)
                number_of_errors += 1
            except jsonschema.exceptions.SchemaError as e:
                print("Schema error: ", e.message)
                number_of_errors += 1
            except jsonschema.exceptions.ValidationError as e:
                print("Validation error: ", e.message)
                number_of_errors += 1
            except json.decoder.JSONDecodeError as e:
                print("Error parsing JSON:", e.msg)
                number_of_errors += 1

        result, schema = ValidateSchema(
            schema_directory="metadata-registry-interface-specifications/metadata/schemas/interface/"
            , resource_directory=json_directory
            , filename=file
            , schema=meta_type
            , version=meta_version
        ).validate()
        name = os.path.basename(file)
        if result:
            type = os.path.basename(schema)
            print(f"VALID: File {name} is a valid {schema}")
        else:
            print(f"INVALID: File {name} does not comply with any schema")
            number_of_errors += 1

    if number_of_files == 0:
        print("No JSON files found in provided JSON directory")
        exit(1)
    else:
        print("Verified >", number_of_files, "< JSON files. Number of errors: ", number_of_errors )
        if number_of_errors > 0:
            exit(2)
        else:
            exit(0)


if __name__ == '__main__':
    main()
