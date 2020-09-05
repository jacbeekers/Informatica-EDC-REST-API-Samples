import glob
import json

from metadata_utilities import check_schema
from metadata_utilities import generic_settings, generic
from metadata_utilities import messages
from metadata_utilities import mu_logging


class ConvertJSONtoEDCLineage:
    """
    Converts JSON file to a csv that can be consumed by Informatica EDC
    """
    code_version = "0.1.0"

    def __init__(self):
        self.json_file = "not provided"
        self.meta_type = "unknown"
        self.result = messages.message["undetermined"]
        self.settings = generic_settings.GenericSettings()
        self.generic = generic.Generic()
        self.json_directory = self.settings.json_directory
        self.target = self.settings.target
        self.overall_result = messages.message["undetermined"]
        self.mu_log = mu_logging.MULogging()

    def generate_file_structure(self):
        """
        Generate the metadata file for the data. The result is a file with only a header. No real data is needed.
        """
        module = "generate_file_structure"
        file_result = messages.message["ok"]
        with open(self.json_file) as entity:
            data = json.load(entity)
        if data["entity_type"] == "file":
            filename = data["name"]
            self.mu_log.log(self.mu_log.DEBUG, "entity type = file. Generating metafile for " + filename)
            entity_uuid = data["uid"]
            # find the entity_uuid in the property physical_entity of a physical_attribute file
            file_result = self.generic.find_json(entity_uuid, "physical_attribute", "physical_entity")
            attributes = self.generic.attribute_list
            if file_result["code"] == "OK":
                file_result = self.create_metafile(filename, attributes)
        else:
            self.mu_log.log(self.mu_log.DEBUG, "entity is not a file. Skipping metafile creation", module)
        return file_result

    def create_metafile(self, filename, attributes):
        """
        A metafile is created for Informatica EDC to scan. This way no real data is needed.
        """
        module = "create_metafile"
        concatenated = self.generic.convert_list_into_string(attributes)
        if self.target == "local":
            file_result = self.generic.write_local_file(filename, concatenated)
        else:
            # TODO: Implement "azure_blob"
            self.mu_log.log(self.mu_log.DEBUG
                            , "In this release the only target is local. In the future Azure Blob will be added."
                            , module)
            file_result = messages.message["not_implemented"]

        return file_result

    def process_files(self):
        """
        Process files in the configued json directory (check config.json)
        For each file: Validate its schema and generate the metadata definition file or lineage file
            (depends on the meta_type of the file found)
        """
        module = "process_files"
        directory = self.settings.json_directory
        for file in glob.glob(directory + "*.json"):
            self.json_file = file
            file_result = messages.message["ok"]
            check = check_schema.CheckSchema()
            check_result = check.check_schema(self.json_file)
            if check_result == "OK":
                self.mu_log.log(self.mu_log.DEBUG, "schema check returned OK", module)
                self.meta_type = check.meta_type
                if self.meta_type == "physical_entity":
                    file_result = self.generate_file_structure()
                elif self.meta_type in ("physical_attribute_association", "physical_entity_association"):
                    file_result = self.process_lineage_request()
                    self.mu_log.log(self.mu_log.DEBUG, f"lineage processing completed with code {file_result['code']}"
                                    , module)
                else:
                    self.mu_log.log(self.mu_log.DEBUG,
                                    "file is not a physical entity or an association. Nothing to do with it."
                                    , module)
                if file_result["code"] == "OK":
                    self.mu_log.log(self.mu_log.DEBUG, "file processed successfully", module)
                else:
                    self.overall_result = file_result
            else:
                self.overall_result = file_result
                self.mu_log.log(self.mu_log.DEBUG, "schema check failed.", module)
        return self.overall_result

    def process_lineage_request(self):
        # Generate the lineage file. May not be needed when using an API
        module = "process_lineage_request"
        overall_result = messages.message["undetermined"]
        csv_result = self.generate_lineage("csv")
        self.mu_log.log(self.mu_log.DEBUG, "csv lineage creation completed with >" + csv_result['code']
                        + "<", module)
        if csv_result["code"] != "OK":
            overall_result = csv_result
        json_result = self.generate_lineage("json_payload")
        if json_result["code"] != "OK":
            overall_result = json_result
        self.mu_log.log(self.mu_log.DEBUG, "json_payload lineage creation completed with >" + json_result['code']
            + "<", module)
        # Send lineage info to metadata target
        send_result = self.send_metadata()
        self.mu_log.log(self.mu_log.DEBUG, "lineage creation completed with >" + send_result['code'] + "<", module)
        if send_result["code"] != "OK":
            overall_result = send_result

        return overall_result

    def generate_lineage(self, type):
        module = "generate_lineage"
        self.mu_log.log(self.mu_log.DEBUG, "generating lineage for " + type, module)

        lineage_result = messages.message["not_implemented"]
        return lineage_result

    def build_api_load(self, metadata_type):
        module = "build_api_load"
        #        self.api_load =
        build_result = messages.message["not_implemented"]
        return build_result

    def send_metadata(self):
        module = "send_metadata"
        target = self.settings.metadata_store
        self.mu_log.log(self.mu_log.DEBUG, "sending lineage info to " + target, module)

        if target == "edc":
            send_result = self.send_metadata_to_edc()
        elif target == "metadata_lake":
            send_result = self.send_metadata_to_metadata_lake()
        else:
            self.mu_log.log(self.mu_log.DEBUG, "unknown metadata target type: " + target, module)
            send_result = messages.message["unknown_metadata_target"]

        return send_result

    def send_metadata_to_edc(self):
        send_result = messages.message["not_implemented"]
        return send_result

    def send_metadata_to_metadata_lake(self):
        send_result = messages.message["not_implemented"]
        return send_result

    def main(self):
        module = "main"
        process_result = self.process_files()
        self.mu_log.log(self.mu_log.INFO, "Result: " + process_result["code"] + " - " + process_result["message"], module)


if __name__ == "__main__":
    result = ConvertJSONtoEDCLineage().main()
