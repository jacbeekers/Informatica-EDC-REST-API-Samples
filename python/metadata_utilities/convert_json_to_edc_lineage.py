import glob
import json

from metadata_utilities import check_schema
from metadata_utilities import messages


class ConvertJSONtoEDCLineage:
    """
    Converts JSON file to a csv that can be consumed by Informatica EDC
    """
    version = "0.1.0"

    def __init__(self):
        self.json_file = "not provided"
        self.meta_type = "unknown"
        self.result = "unknown"

    def generate_file_structure(self):
        file_result = "unknown"
        with open(self.json_file) as entity:
            data = json.load(entity)
        if data["entity_type"] == "file":
            filename = data["name"]
            print("entity type = file. Generating metafile for " + filename)
            entity_uuid = data["uid"]
            file_result, attributes = self.get_entity_attributes(entity_uuid)
            print(attributes)
            if file_result == "OK":
                file_result = self.create_metafile(filename, attributes)
        else:
            print("entity is not a file. Skipping metafile creation")
        return file_result

    def get_entity_attributes(self, entity_uuid):
        # TODO: Find the corresponding attribute file
        #   use the uuid of the entity
        #   filter on json files of meta_type physical_attribute
        attribute_list = ["col1", "col2"]
        return messages.message["ok"]["code"], attribute_list

    def create_metafile(self, filename, attributes):
        """
        A metafile is created for Informatica EDC to scan. This way no real data is needed.
        """
        concatenated = ""
        nr_cols = 0
        for attribute in attributes:
            nr_cols += 1
            if nr_cols == 1:
                concatenated = attribute
            else:
                concatenated += "," + attribute

        # local file system
        # TODO: Write to Azure Blob Storage
        with open(filename, "w") as f:
            f.write(concatenated)

        print("file successfully created")
        return "OK"

    def main(self):
        directory = "resources/Datalineage and metadata/JSON files/"
        for file in glob.glob(directory + "*.json"):
            self.json_file = file
            check = check_schema.CheckSchema()
            file_result = check.check_schema(self.json_file)
            if file_result == "OK":
                print("schema check returned OK")
                self.meta_type = check.meta_type
                if self.meta_type == "physical_entity":
                    file_result = self.generate_file_structure()
                if self.meta_type in ("physical_attribute_association", "physical_entity_association"):
                    print("Generating lineage file")
                    # TODO: Generate it
                if file_result == "OK":
                    print("file processed successfully")
                else:
                    self.result = file_result
            else:
                self.result = file_result
                print("schema check failed.")
        return self.result


if __name__ == "__main__":
    result = ConvertJSONtoEDCLineage().main()
    print(f"Result: {result}")
