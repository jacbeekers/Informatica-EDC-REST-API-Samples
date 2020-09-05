import glob
import json

from metadata_utilities import check_schema
from metadata_utilities import generic
from metadata_utilities import messages


class ConvertJSONtoEDCLineage:
    """
    Converts JSON file to a csv that can be consumed by Informatica EDC
    """
    version = "0.1.0"

    def __init__(self):
        self.json_file = "not provided"
        self.meta_type = "unknown"
        self.result = messages.message["undetermined"]
        self.generic = generic.Generic()
        self.json_directory = self.generic.json_directory
        self.target = self.generic.target
        self.overall_result = messages.message["undetermined"]

    def generate_file_structure(self):
        """
        Generate the metadata file for the data. The result is a file with only a header. No real data is needed.
        """
        file_result = messages.message["ok"]
        with open(self.json_file) as entity:
            data = json.load(entity)
        if data["entity_type"] == "file":
            filename = data["name"]
            print("entity type = file. Generating metafile for " + filename)
            entity_uuid = data["uid"]
            # find the entity_uuid in the property physical_entity of a physical_attribute file
            file_result = self.generic.find_json(entity_uuid, "physical_attribute", "physical_entity")
            attributes = self.generic.attribute_list
            if file_result["code"] == "OK":
                file_result = self.create_metafile(filename, attributes)
        else:
            print("entity is not a file. Skipping metafile creation")
        return file_result

    def create_metafile(self, filename, attributes):
        """
        A metafile is created for Informatica EDC to scan. This way no real data is needed.
        """
        concatenated = self.generic.convert_list_into_string(attributes)
        if self.target == "local":
            file_result = self.generic.write_local_file(filename, concatenated)
        else:
            # TODO: Implement "azure_blob"
            print("In this release the only target is local. In the future Azure Blob will be added.")
            file_result = messages.message["not_implemented"]

        return file_result

    def process_files(self):
        """
        Process files in the configued json directory (check config.json)
        For each file: Validate its schema and generate the metadata definition file or lineage file
            (depends on the meta_type of the file found)
        """
        directory = self.generic.json_directory
        for file in glob.glob(directory + "*.json"):
            self.json_file = file
            file_result = messages.message["ok"]
            check = check_schema.CheckSchema()
            check_result = check.check_schema(self.json_file)
            if check_result == "OK":
                print("schema check returned OK")
                self.meta_type = check.meta_type
                if self.meta_type == "physical_entity":
                    file_result = self.generate_file_structure()
                elif self.meta_type in ("physical_attribute_association", "physical_entity_association"):
                    file_result = self.process_lineage_request()
                    print(f"lineage processing completed with code {file_result['code']}")
                else:
                    print("file is not a physical entity or an association. Nothing to do with it.")
                if file_result["code"] == "OK":
                    print("file processed successfully")
                else:
                    self.overall_result = file_result
            else:
                self.overall_result = file_result
                print("schema check failed.")
        return self.overall_result

    def process_lineage_request(self):
        overall_result = messages.message["undetermined"]
        # Generate the lineage file. May not be needed when using an API
        csv_result = self.generate_lineage("csv")
        print(f"\tcsv lineage creation completed with {csv_result['code']}")
        if csv_result["code"] != "OK":
            overall_result = csv_result
        json_result = self.generate_lineage("json_payload")
        if json_result["code"] != "OK":
            overall_result = json_result
        print(f"\tjson_payload lineage creation completed with {json_result['code']}")
        # Send lineage info to metadata target
        send_result = self.send_metadata()
        print(f"\tlineage creation completed with {send_result['code']}")
        if send_result["code"] != "OK":
            overall_result = send_result

        return overall_result

    def generate_lineage(self, type):
        print(f"\tgenerating lineage for {type}")

        lineage_result = messages.message["not_implemented"]
        return lineage_result

    def build_api_load(self, metadata_type):
#        self.api_load =
        build_result = messages.message["not_implemented"]
        return build_result

    def send_metadata(self):
        target = self.generic.metadata_store
        print(f"\tsending lineage info to {target}")

        if target == "edc":
            send_result = self.send_metadata_to_edc()
        elif target == "metadata_lake":
            send_result = self.send_metadata_to_metadata_lake()
        else:
            print(f"unknown metadata target type: " + target)
            send_result = messages.message["unknown_metadata_target"]

        return send_result

    def send_metadata_to_edc(self):
        send_result = messages.message["not_implemented"]
        return send_result

    def send_metadata_to_metadata_lake(self):
        send_result = messages.message["not_implemented"]
        return send_result

    def main(self):
        return self.process_files()


if __name__ == "__main__":
    result = ConvertJSONtoEDCLineage().main()
    print("Result: " + result["code"] + " - " + result["message"])
