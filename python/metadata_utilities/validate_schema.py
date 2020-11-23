import glob
import json
import os

import jsonschema


class ValidateSchema():
    default_version = "0.2.0"
    default_schema_directory = "metadata/schemas/interface/" + default_version + "/"
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

        with open(self.verify_file) as file:
            name = os.path.basename(file.name)
            print(f"Verifying {name}")
            the_doc = json.load(file)

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

        return False, "None"


if __name__ == '__main__':

    json_directory = "."
    print("JSON directory is: " + json_directory)
    for file in glob.glob(json_directory + "*.json"):
        with open(file) as f:
            the_schema = json.load(f)
            try:
                meta_type = the_schema["meta"]
                meta_version = the_schema["meta_version"]
                print("schema is " + meta_type + " version " + meta_version)
            except KeyError as e:
                print("Key error. meta and meta_version must be in JSON file. That is not the case with " + file)
            except jsonschema.exceptions.SchemaError as e:
                print("Schema error: ", e.message)
            except jsonschema.exceptions.ValidationError as e:
                print("Validation error: ", e.message)
            except json.decoder.JSONDecodeError as e:
                print("Error parsing JSON:", e.msg)

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
