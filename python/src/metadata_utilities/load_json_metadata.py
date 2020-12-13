import glob
import json
import os

from src.edc_utilities import edc_custom_attributes
from src.edc_utilities import edc_lineage
from src.metadata_utilities import check_schema
from src.metadata_utilities import generic_settings, generic
from src.metadata_utilities import messages
from src.metadata_utilities import mu_logging, json_file_utilities


class ConvertJSONtoEDCLineage:
    """
    Converts JSON file to a JSON payload that can be send to Informatica EDC using its APIs
    """
    code_version = "0.2.15"

    def __init__(self, configuration_file="resources/config.json"):
        self.json_file = "not provided"
        self.meta_type = "unknown"
        self.result = messages.message["undetermined"]
        self.settings = generic_settings.GenericSettings(configuration_file)
        self.config_result = self.settings.get_config()
        self.edc_custom_attributes = edc_custom_attributes.EDCCustomAttribute()

        if self.config_result == messages.message["ok"]:
            self.mu_log = mu_logging.MULogging(self.settings.log_config)
            self.generic = generic.Generic(settings=self.settings, mu_log_ref=self.mu_log)
            self.json_directory = self.settings.json_directory
            self.target = self.settings.target
            self.overall_result = messages.message["ok"]
            # For Azure Monitor
            self.mu_log.code_version = self.code_version
            self.json_file_utilities = json_file_utilities.JSONFileUtilities()
            self.data = ""
            self.edc_lineage = edc_lineage.EDCLineage(self.settings, mu_log_ref=self.mu_log)
        else:
            print("FATAL:", "settings.get_config returned:",
                  self.config_result["code"] + " - " + self.config_result["message"])

    def generate_file_structure(self):
        """
        Generate the metadata file for the data. The result is a file with only a header. No real data is needed.
        """
        module = "ConvertJSONtoEDCLineage.generate_file_structure"
        file_result = messages.message["ok"]
        with open(self.json_file) as entity:
            data = json.load(entity)
        if data["entity_type"] == "file":
            filename = data["name"]
            self.mu_log.log(self.mu_log.DEBUG, "entity type = file. Generating metafile for " + filename, module)
            entity_uuid = data["uid"]
            # find the entity_uuid in the property physical_entity of a physical_attribute file
            file_result = self.generic.find_json(entity_uuid, "physical_attribute", "physical_entity"
                                                 , log_prefix="find entity " + entity_uuid + " - ")
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
        module = "ConvertJSONtoEDCLineage.create_metafile"
        self.mu_log.log(self.mu_log.DEBUG, "Start writing file", module)
        concatenated = self.generic.convert_list_into_string(attributes)
        if self.settings.target == "local":
            file_result = self.generic.write_local_file(filename, concatenated)
        else:
            # TODO: Implement "azure_blob"
            self.mu_log.log(self.mu_log.DEBUG
                            , "In this release the only target is local. In the future Azure Blob will be added."
                            , module)
            file_result = messages.message["not_implemented"]

        self.mu_log.log(self.mu_log.DEBUG, "End writing file", module)
        return file_result

    def process_files(self):
        """
        Process files in the configued json directory (check config.json)
        For each file: Validate its schema and generate the metadata definition file or lineage file
            (depends on the meta_type of the file found)
        """
        module = "ConvertJSONtoEDCLineage.process_files"
        if self.config_result != messages.message["ok"]:
            return self.config_result
        else:
            self.mu_log.log(self.mu_log.DEBUG, "Configuration file >" + self.settings.main_config_file
                            + "< found and read.", module)

        directory = self.settings.json_directory
        self.mu_log.log(self.mu_log.INFO, "===============================================", module)
        self.mu_log.log(self.mu_log.INFO, "Processing JSON files in directory " + directory, module)
        self.mu_log.log(self.mu_log.INFO, "===============================================", module)
        number_of_files = 0
        for file in glob.glob(directory + "*.json"):
            number_of_files += 1
            self.json_file = file
            base_filename = os.path.splitext(os.path.basename(self.json_file))[0]
            self.mu_log.area = base_filename
            self.mu_log.log(self.mu_log.INFO, "#" + str(number_of_files) + " JSON file is: " + self.json_file, module)
            self.data = self.json_file_utilities.get_json(self.json_file)
            file_result = messages.message["ok"]
            check = check_schema.CheckSchema(self.settings, self.mu_log)
            check.mu_log.area = base_filename
            check_result = check.check_schema(self.data)
            if check_result == messages.message["ok"]:
                self.mu_log.log(self.mu_log.DEBUG, "schema check returned OK", module)
                self.meta_type = check.meta_type
                file_result = self.process_physical_entity_and_attribute()
                if file_result == messages.message["ok"]:
                    self.mu_log.log(self.mu_log.DEBUG, "file processed successfully", module)
                else:
                    self.overall_result = file_result
            else:
                self.overall_result = check_result
                self.mu_log.log(self.mu_log.DEBUG, "schema check failed with: " + check_result["code"] + " - "
                                + check_result["message"], module)
            self.mu_log.log(self.mu_log.INFO, "=== END ============================================", module)
        self.mu_log.area = "conclusion"
        self.mu_log.log(self.mu_log.INFO, "Number of JSON files processed: " + str(number_of_files), module)
        return self.overall_result

    def process_physical_entity_and_attribute(self):
        """
        Generate metadata files to be parsed by EDC
        """
        file_result = messages.message["ok"]
        module = "ConvertJSONtoEDCLineage.process_physical_entity_and_attribute"

        if self.meta_type not in ("physical_entity", "physical_entity_association", "physical_attribute_association"):
            self.mu_log.log(self.mu_log.DEBUG,
                            "file is not a physical entity or an association. File ignored."
                            , module)
            return file_result

        if self.meta_type == "physical_entity":
            file_result = self.generate_file_structure()
            return file_result

        # if self.meta_type == "physical_attribute_association":
        #    file_result = self.generate_transformations()
        #    self.mu_log.log(self.mu_log.DEBUG, "The generation of transformation files returned >"
        #                    + file_result['code'] + "<"
        #                    , module)

        if self.meta_type in ("physical_attribute_association", "physical_entity_association"):
            file_result = self.process_lineage_request()
            self.mu_log.log(self.mu_log.DEBUG, "lineage processing completed with code >"
                            + file_result['code'] + "<" + " - " + file_result["message"]
                            , module)

        if self.meta_type == "physical_attribute_association":
            result = self.edc_lineage.update_object_attributes(entity_type=self.meta_type
                                                               , data=self.data
                                                               , settings=self.settings)
            self.mu_log.log(self.mu_log.DEBUG, "update_object_attributes returned: " + result["code"], module)
            file_result = result

        return file_result

    def generate_transformations(self):
        """
        generate a transformation file for each encountered transformation in the attribute_association json
        """
        module = __name__ + ".generate_transformations"
        overall_result = messages.message["ok"]
        if not "source_target_attribute_links" in self.data:
            self.mu_log.log(self.mu_log.DEBUG,
                            "did not find source_target_attribute_links. Transformation processing suppressed.", module)
            return messages.message["ok"]

        self.mu_log.log(self.mu_log.DEBUG, "found source_target_attribute_links", module)
        link_number = 0
        for link in self.data["source_target_attribute_links"]:
            link_number += 1
            if "transformation" in link:
                if "uid" in link["transformation"]:
                    self.mu_log.log(self.mu_log.DEBUG, "found transformation >" + link["transformation"]["uid"] + "<",
                                    module)
                    if "from" in link["transformation"]:
                        source_attributes = link["transformation"]["from"]
                        self.mu_log.log(self.mu_log.DEBUG, "# source attributes: " + str(len(source_attributes)),
                                        module)
                        for source_attribute in source_attributes:
                            self.mu_log.log(self.mu_log.VERBOSE, "source attribute: " + source_attribute, module)
                    else:
                        self.mu_log.log(self.mu_log.INFO,
                                        "No source attributes provided. Assuming attribute is target-only.", module)
                    if "to" in link["transformation"]:
                        self.mu_log.log(self.mu_log.DEBUG, "target attribute: " + link["transformation"]["to"], module)
                    else:
                        self.mu_log.log(self.mu_log.INFO,
                                        "No target attribute provided. Assuming attribute is source-only.", module)
                    if "description" in link:
                        self.mu_log.log(self.mu_log.VERBOSE, "description: " + link["description"], module)
                    else:
                        self.mu_log.log(self.mu_log.DEBUG, "No description provided, which is ok.", module)
                    if "formula" in link:
                        self.mu_log.log(self.mu_log.VERBOSE, "formula: " + link["formula"], module)

                    else:
                        self.mu_log.log(self.mu_log.INFO, "No formula provided, which is ok.", module)
                else:
                    self.mu_log.log(self.mu_log.ERROR, "transformation in link# " + str(link_number)
                                    + " does not contain a uid.", module)
                    overall_result = messages.message["missing_uid"]
            else:
                self.mu_log.log(self.mu_log.WARNING,
                                "WARNING: No transformation info provided in link# " + str(link_number)
                                + ". Transformation handling for source/target attributes surpressed.", module)

        return overall_result

    def process_lineage_request(self):
        # Generate the lineage file or payload
        module = __name__ + ".process_lineage_request"
        # TODO: generate json payload for the Metadata Interface APIs for lineage
        #       something like this:
        #           json_result = self.metadata_lake_lineage.generate_lineage("json_payload", self.meta_type, self.data)
        self.edc_lineage.mu_log.area = self.mu_log.area
        response = None

        result, payload = self.edc_lineage.generate_lineage(
            output_type="json_payload"
            , metadata_type=self.meta_type
            , data=self.data
            , generic_settings=self.settings)

        # payload was generated
        if result == messages.message["ok"]:
            self.mu_log.log(self.mu_log.DEBUG, "sending lineage info to " + self.settings.metadata_store, module)
            # In 2020 only EDC is supported. Later, other targets can be included
            if self.settings.metadata_store == "edc":
                result, response = self.edc_lineage.send_metadata_to_edc(
                    suppress_edc_call=self.settings.suppress_edc_call
                    , method="PATCH"
                    , uri="/access/1/catalog/data/objects"
                    , payload=payload
                )
            elif self.settings.metadata_store == "metadata_lake":
                result = self.send_metadata_to_metadata_lake()
            else:
                self.mu_log.log(self.mu_log.ERROR, "Invalid target specified: " + self.settings.metadata_store, module)
                send_result = messages.message["unknown_metadata_target"]
            self.mu_log.log(self.mu_log.DEBUG, "lineage creation completed with >" + result['code'] + "<", module)
        else:
            self.mu_log.log(self.mu_log.ERROR, "json_payload lineage creation completed with >" + result['code']
                            + "<", module)

        return result

    def send_metadata_to_metadata_lake(self):
        module = "ConvertJSONtoEDCLineage.send_metadata_to_metadata_lake"
        self.mu_log.log(self.mu_log.ERROR, "Function >" + module + "< is not implemented.", module)
        send_result = messages.message["not_implemented"]
        return send_result

    def main(self):
        """
            Main module to process JSON files that are stored at the location stated in the provided configuration file
            configuration_file: a relative or absolute path to the configuration file. Default is resources/config.json
        """
        module = "ConvertJSONtoEDCLineage.main"
        process_result = self.process_files()
        return process_result


if __name__ == "__main__":
    """
        Call to main without any arguments reads the resources/config.json file to determine directories and other settings
    """
    result = ConvertJSONtoEDCLineage().main()
    if result["code"] != "OK":
        exit(1)
    else:
        exit(0)
