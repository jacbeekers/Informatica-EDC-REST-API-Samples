import jsonschema
import json
from pathlib import Path
import glob
import os

class ValidateSchema():

    default_version = "0.2.0"
    default_schema_directory = "metadata-registry-interface-specifications/metadata/schemas/interface/" + default_version + "/"
    default_schema = "physical_entity.json"
    default_resource_directory = "metadata/resources/"
    default_filename = "default.json"

    def __init__(self
                 , schema_directory=default_schema_directory
                 , schema = default_schema
                 , version=default_version
                 , resource_directory=default_resource_directory
                 , filename=default_filename):
        self.version = version
        self.schema_directory = schema_directory
        self.schema = schema
        self.against_schema = self.schema_directory + "physical_entity.json"
        self.resource_directory = resource_directory + "/"
        self.filename = filename
        self.verify_file = self.resource_directory + self.filename

    def validate(self):

        with open(self.verify_file) as file:
            name = os.path.basename(file.name)
            print(f"Verifying {name}")
            the_doc = json.load(file)

            for schema in glob.glob(self.schema_directory + "*.json"):
                with open(schema) as structure:
                    struct = os.path.basename(structure.name)
                    print(f"\t\t against {struct}")
                    try:
                        the_schema = json.load(structure)
                        jsonschema.validate(the_doc, the_schema)
                        return True, schema
                    except jsonschema.exceptions.ValidationError as e:
                        print(f"\t\t Validation error:{e.message} ")
                    except json.decoder.JSONDecodeError as e:
                        print(f"\t\t ERROR parsing JSON:{e.msg} line {e.lineno} col {e.colno}")
        return False, "None"


if __name__ == '__main__':

    directory = "resources/Datalineage and metadata/JSON files/"
    for file in glob.glob(directory + "*.json"):
        result, schema = ValidateSchema(resource_directory=".", filename=file).validate()
        name = os.path.basename(file)
        if result:
            type = os.path.basename(schema)
            print(f"VALID: File {name} is a valid {schema}")
        else:
            print(f"INVALID: File {name} does not comply with any schema")
