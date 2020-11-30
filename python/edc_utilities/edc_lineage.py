import json
import time

import jinja2

from edc_utilities import edcSessionHelper
from metadata_utilities import mu_logging, generic_settings, messages, generic


class EDCLineage:
    """
    EDLineage: Call Informatica EDC APIs to add lineage information for existing objects
    """

    code_version = "0.1.0"
    total = 1000

    def __init__(self):
        self.offset = 0
        self.page = 0
        self.mu_log = mu_logging.MULogging()
        self.settings = generic_settings.GenericSettings()
        self.edc_source_filesystem = self.settings.edc_config_data["edc_source_filesystem"]
        self.edc_source_datasource = self.settings.edc_config_data["edc_source_datasource"]
        self.edc_source_folder = self.settings.edc_config_data["edc_source_folder"]
        self.edc_target_filesystem = self.settings.edc_config_data["edc_target_filesystem"]
        self.edc_target_datasource = self.settings.edc_config_data["edc_target_datasource"]
        self.edc_target_folder = self.settings.edc_config_data["edc_target_folder"]
        self.generic = generic.Generic()
        self.edc_helper = edcSessionHelper.EDCSession()
        # TODO: Get info from jinja_config mentioned in config.json
        self.application = "edc_utilities"
        self.templates = "edc_payload_templates"
        self.environment = jinja2.Environment(loader=jinja2.PackageLoader(self.application, self.templates))
        self.environment.filters["jsonify"] = json.dumps
        self.template = self.environment.get_template("physical_entity_association.json")
        self.meta_type = "unknown"
        self.payload = "{}"

    def generate_lineage(self, output_type, metadata_type, data):
        module = "generate_lineage"
        self.meta_type = metadata_type
        self.data = data
        if output_type == "json_payload":
            self.mu_log.log(self.mu_log.DEBUG, "generating lineage for output_type " + output_type, module)
            lineage_result, payload = self.build_api_load()
        elif output_type == "csv":
            lineage_result = messages.message["not_implemented"]
        else:
            self.mu_log.log(self.mu_log.ERROR, "invalid lineage output_type >" + output_type + "< specified.", module)
            lineage_result = messages.message["invalid_lineage_output_type"]

        return lineage_result

    def build_api_load(self):
        module = "build_api_load"
        self.template = self.environment.get_template(self.meta_type + ".json")
        if self.meta_type == "physical_entity_association":
            build_result, self.payload = self.build_api_load_entity_association()
        elif self.meta_type == "physical_attribute_association":
            build_result, self.payload = self.build_api_load_attribute_association()
        else:
            build_result = messages.message["unknown_metadata_target"]
            self.payload = "{}"

        self.mu_log.log(self.mu_log.VERBOSE, "payload: " + self.payload, module)
        return build_result, self.payload

    def build_api_load_entity_association(self):
        """
        Loop through the list of source_target_entities
        """
        module = "build_api_load_entity_association"
        build_result = messages.message["ok"]
        source_target_links = self.data["source_target_entity_links"]
        source_target_list = []
        update_entry_list = []

        template_updates = self.environment.get_template("physical_association_updates.jinja2")
        template_update_entry = self.environment.get_template("physical_association_update_entry.jinja2")
        template_new_sourcelinks = self.environment.get_template("physical_association_source_link.jinja2")
        target = ""
        for source_target_entity in source_target_links:
            self.mu_log.log(self.mu_log.DEBUG, "entity link from >" + source_target_entity["from"] + "< to >"
                            + source_target_entity["to"] + "<", module)
            find_result = self.generic.find_json(source_target_entity["from"], "physical_entity", "uid"
                                                 , log_prefix="from " + source_target_entity["from"] + " - ")
            if find_result["code"] != "OK":
                self.mu_log.log(self.mu_log.ERROR,
                                "The entity association contains a source UUID that could not be found in any entity JSON file.")
                build_result = messages.message["json_uuid_not_found"]
                return build_result, "{}"

            source_name = self.generic.found_data["name"]
            from_dataset = self.edc_source_filesystem \
                           + self.edc_source_datasource \
                           + self.edc_source_folder \
                           + source_name
            new_entry = template_new_sourcelinks.render(source_object_id=from_dataset, data_flow="core.DataSetDataFlow")
            self.mu_log.log(self.mu_log.VERBOSE, "new entry: " + new_entry, module)
            source_target_list.append(new_entry)

            find_result = self.generic.find_json(source_target_entity["to"], "physical_entity", "uid"
                                                 , log_prefix="to " + source_target_entity["to"] + " - ")
            if find_result["code"] != "OK":
                self.mu_log.log(self.mu_log.ERROR,
                                "The entity association contains a target UUID that could not be found in any entity JSON file.")
                build_result = messages.message["json_uuid_not_found"]
                return build_result, "{}"

            target_name = self.generic.found_data["name"]
            target = self.edc_target_filesystem \
                     + self.edc_target_datasource \
                     + self.edc_target_folder \
                     + target_name

        the_source_targets = ",".join(source_target_list)
        self.mu_log.log(self.mu_log.VERBOSE, "source_targets combined: " + the_source_targets, module)

        update_entry = template_update_entry.render(new_sourcelinks=the_source_targets, target_object_id=target)
        update_entry_list.append(update_entry)
        the_entries = ",".join(update_entry_list)
        self.payload = template_updates.render(update_entries=the_entries)
        self.mu_log.log(self.mu_log.VERBOSE, "payload: " + self.payload, module)

        return build_result, self.payload

    def build_api_load_attribute_association(self):
        """
        Loop through the list of source_target_attributes
        """
        module = "build_api_load_attribute_association"
        build_result = messages.message["ok"]
        source_target_links = self.data["source_target_attribute_links"]
        source_target_list = []
        update_entry_list = []

        template_updates = self.environment.get_template("physical_association_updates.jinja2")
        template_update_entry = self.environment.get_template("physical_association_update_entry.jinja2")
        template_new_source_links = self.environment.get_template("physical_association_source_link.jinja2")

        to_entity_name = "NONE"
        for source_target in source_target_links:
            source_target_list = []
            transformation = source_target["transformation"]
            to_attribute_uuid = transformation["to"]
            self.mu_log.log(self.mu_log.DEBUG, "processing to_attribute_uuid: " + to_attribute_uuid, module)
            find_result = self.generic.find_json(to_attribute_uuid, "physical_attribute", "uid"
                                                 , log_prefix="to_attribute_uuid " + to_attribute_uuid + " - ")
            if find_result["code"] != "OK":
                self.mu_log.log(self.mu_log.ERROR,
                                "The attribute association contains a target UUID that could not be found in any attribute JSON file."
                                , module)
                build_result = messages.message["json_uuid_not_found"]
                return build_result, "{}"

            to_attribute_data = self.generic.found_data
            to_attribute_index = self.generic.index
            to_attribute_name = to_attribute_data["attribute_list"][to_attribute_index]["name"]
            self.mu_log.log(self.mu_log.DEBUG, "to_attribute_name is: " + to_attribute_name, module)
            to_entity_uuid = to_attribute_data["physical_entity"]
            find_result = self.generic.find_json(to_entity_uuid, "physical_entity", "uid",
                                                 log_prefix="to_entity_uuid " + to_entity_uuid + " - ")
            if find_result["code"] != "OK":
                self.mu_log.log(self.mu_log.ERROR,
                                "The 'to' attribute contains an entity UUID that could not be found in any entities JSON file."
                                , module)
                build_result = messages.message["json_uuid_not_found"]
                return build_result, "{}"

            to_entity_data = self.generic.found_data
            to_entity_name = to_entity_data["name"]
            to_attribute = self.edc_target_filesystem \
                           + self.edc_target_datasource \
                           + self.edc_target_folder \
                           + to_entity_name \
                           + "/" \
                           + to_attribute_name
            self.mu_log.log(self.mu_log.DEBUG, "attribute id in EDC is >" + to_attribute + "<", module)

            from_attribute_list = transformation["from"]
            self.mu_log.log(self.mu_log.DEBUG, "from attribute(s) >" + str(from_attribute_list) + "< to >"
                            + to_attribute + "<", module)

            self.mu_log.log(self.mu_log.DEBUG, "number of entries in attribute list: " + str(len(from_attribute_list)),
                            module)
            if len(from_attribute_list) == 0:
                new_entry = template_new_source_links.render(source_object_id=to_attribute,
                                                             data_flow="core.DirectionalDataFlow")
                self.mu_log.log(self.mu_log.VERBOSE, "new entry: " + new_entry, module)
                source_target_list.append(new_entry)

            i = 0
            for attribute in from_attribute_list:
                i += 1
                nr = str(i).zfill(3) + ": "
                self.mu_log.log(self.mu_log.VERBOSE, nr + "current attribute: " + attribute, module)
                find_result = self.generic.find_json(attribute, "physical_attribute", "uid", log_prefix=nr)
                if find_result["code"] != "OK":
                    self.mu_log.log(self.mu_log.ERROR, nr +
                                    "The attribute association contains a source UUID that could not be found in any attribute JSON file."
                                    , module)
                    build_result = messages.message["json_uuid_not_found"]
                    return build_result, "{}"

                attribute_data = self.generic.found_data
                attribute_index = self.generic.index

                find_result = self.generic.find_json(attribute_data["physical_entity"], "physical_entity", "uid"
                                                     , log_prefix=nr + " entity " + attribute_data[
                        "physical_entity"] + " - ")
                if find_result["code"] != "OK":
                    self.mu_log.log(self.mu_log.ERROR, nr +
                                    "The attribute association contains a physical entity UUID that could not be found in any entity JSON file."
                                    , module)
                    build_result = messages.message["json_uuid_not_found"]
                    return build_result, "{}"

                entity_data = self.generic.found_data
                source_name = self.edc_source_filesystem \
                              + self.edc_source_datasource \
                              + self.edc_source_folder \
                              + entity_data["name"] \
                              + "/" \
                              + attribute_data["attribute_list"][attribute_index]["name"]
                self.mu_log.log(self.mu_log.DEBUG, nr + "attribute name is >" + str(source_name) + "<", module)

                new_entry = template_new_source_links.render(source_object_id=source_name,
                                                             data_flow="core.DirectionalDataFlow")
                self.mu_log.log(self.mu_log.VERBOSE, nr + "new entry: " + new_entry, module)
                source_target_list.append(new_entry)

            the_source_targets = ",".join(source_target_list)
            self.mu_log.log(self.mu_log.VERBOSE, "source_targets combined: " + the_source_targets, module)
            update_entry = template_update_entry.render(new_sourcelinks=the_source_targets,
                                                        target_object_id=to_attribute)
            update_entry_list.append(update_entry)

        the_entries = ",".join(update_entry_list)
        self.payload = template_updates.render(update_entries=the_entries)
        # TODO: Find a good solution for this
        self.payload = self.payload.replace("<<NONE>>", self.edc_target_filesystem
                                            + self.edc_target_datasource
                                            + self.edc_target_folder
                                            + to_entity_name)
        self.mu_log.log(self.mu_log.VERBOSE, "payload: " + self.payload, module)

        return build_result, self.payload

    def send_metadata_to_edc(self, suppress_edc_call=False):
        module = "send_metadata_to_edc"
        self.mu_log.log(self.mu_log.VERBOSE, "sending payload >" + self.payload + "<.", module)
        start_time = time.time()
        self.edc_helper.initUrlAndSessionFromEDCSettings()

        url = self.edc_helper.baseUrl + "/access/1/catalog/data/objects"
        self.mu_log.log(self.mu_log.VERBOSE, "Used URL >" + url + "<.", module)
        head = {'Content-Type': 'application/json'}
        if suppress_edc_call:
            self.mu_log.log(self.mu_log.WARNING
                            , "'suppress_edc_call' is set to True in config.json. EDC call NOT exucuted", module)
            send_result = messages.message["ok"]
        else:
            response = self.edc_helper.session.patch(url, self.payload, timeout=20, headers=head)
            status = response.status_code
            if status != 200:
                # some error - e.g. catalog not running, or bad credentials
                self.mu_log.log(self.mu_log.ERROR, "Error from EDC: " + str(status) + ": " + str(response), module)
                send_result = messages.message["edc_error"]
            else:
                try:
                    result_json = response.json()
                    self.mu_log.log(self.mu_log.INFO, "EDC returned: " + str(result_json), module)
                    send_result = messages.message["ok"]
                except ValueError:
                    self.mu_log.log(self.mu_log.ERROR, "EDC API did not return a JSON payload")
                    send_result = messages.message["invalid_api_response"]

        run_time = time.time() - start_time
        self.mu_log.log(self.mu_log.DEBUG,
                        "send to EDC completed with " + send_result["code"] + ". run time: " + str(run_time), module)
        return send_result


if __name__ == "__main__":
    edc_lineage = EDCLineage()
    edc_lineage.meta_type = "physical_database_association"
    source = "demoSource"
    target = "demoTarget"
    edc_lineage.data = ""
    edc_lineage.build_api_load()

    edc_lineage.meta_type = "physical_schema_association"
    source = "demoSource://demoSource/dbo"
    target = "demoTarget://demotarget/dbo"
    edc_lineage.build_api_load()

    edc_lineage.meta_type = "physical_entity_association"
    source = "demoSource://demoSource/dbo/tblMetaDemo"
    target = "demoTarget://demotarget/dbo/tblMetaDemo"
    edc_lineage.build_api_load()

    # TODO: For all columns
    edc_lineage.meta_type = "physical_attribute_association"
    source = "demoSource://demoSource/dbo/tblMetaDemo/ActiveFrom"
    target = "demoTarget://demotarget/dbo/tblMetaDemo/ActiveFrom"
    edc_lineage.build_api_load()
