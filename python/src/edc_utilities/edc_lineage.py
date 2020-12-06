import json
import time

import jinja2

from src.edc_utilities import edcSessionHelper
from src.metadata_utilities import messages, generic


class EDCLineage:
    """
    EDLineage: Call Informatica EDC APIs to add lineage information for existing objects
    """

    code_version = "0.2.21"
    total = 1000

    def __init__(self, settings, mu_log_ref):
        self.offset = 0
        self.page = 0
        self.settings = settings
        self.mu_log = mu_log_ref
        self.generic = None
        self.edc_source_filesystem = "unknown"
        self.edc_source_datasource = "unknown"
        self.edc_source_folder = "unknown"
        self.edc_target_filesystem = "unknown"
        self.edc_target_datasource = "unknown"
        self.edc_target_folder = "unknown"
        self.edc_helper = edcSessionHelper.EDCSession(self.settings)
        self.proxies = "unknown"
        self.jinja_base_directory = None
        self.jinja_application = None
        self.jinja_templates = None
        self.jinja_template_directory = None
        self.jinja_environment = None
        self.meta_type = "unknown"
        self.payload = {}
        self.data = None
        self.jinja_configuration_file = self.settings.jinja_config

    def generate_lineage(self, output_type, metadata_type, data, generic_settings):
        module = "EDCLineage.generate_lineage"
        if generic_settings is None:
            self.mu_log.log(self.mu_log.DEBUG, "Loading generic settings.", module)
            result = self.settings.get_config()
            if result != messages.message["ok"]:
                self.mu_log.log(self.mu_log.FATAL, "Could not find main configuration file >" + self.settings.json_file + "<."
                                , module)
                return messages.message["main_config_not_found"]
        else:
            self.mu_log.log(self.mu_log.DEBUG, "Generic settings already loaded.", module)
            self.settings = generic_settings

        # Get jinja configuration
        result = self.get_jinja_settings(self.settings)
        if result == messages.message["ok"]:
            self.mu_log.log(self.mu_log.INFO, "Jinja configuration file found and read.", module)
        else:
            self.mu_log.log(self.mu_log.ERROR, "get_jinja_settings returned: " + result["code"], module)
            return result

        self.generic = generic.Generic(settings=self.settings, mu_log_ref=self.mu_log)
        self.proxies = self.settings.get_edc_proxy()
        self.edc_source_filesystem = self.settings.edc_config_data["edc_source_filesystem"]
        self.edc_source_datasource = self.settings.edc_config_data["edc_source_datasource"]
        self.edc_source_folder = self.settings.edc_config_data["edc_source_folder"]
        self.edc_target_filesystem = self.settings.edc_config_data["edc_target_filesystem"]
        self.edc_target_datasource = self.settings.edc_config_data["edc_target_datasource"]
        self.edc_target_folder = self.settings.edc_config_data["edc_target_folder"]

        self.meta_type = metadata_type
        self.data = data
        if output_type == "json_payload":
            self.mu_log.log(self.mu_log.DEBUG, "generating lineage for output_type " + output_type, module)
            lineage_result, payload = self.build_api_load()
        elif output_type == "csv":
            self.mu_log.log(self.mu_log.ERROR, "output_type csv has not been implemented.", module)
            lineage_result = messages.message["not_implemented"]
        else:
            self.mu_log.log(self.mu_log.ERROR, "invalid lineage output_type >" + output_type + "< specified.", module)
            lineage_result = messages.message["invalid_lineage_output_type"]

        return lineage_result

    def get_jinja_settings(self, generic_settings):
        """
            Get the Jinja settings from the provided jinja configuration file: jinja_config key in main config.json
        """
        module = "edc_lineage.get_jinja_settings"
        result = messages.message["ok"]
        try:
            with open(self.jinja_configuration_file) as jinja:
                data = json.load(jinja)
                if "base_directory" in data:
                    self.jinja_base_directory = data["base_directory"]
                    self.mu_log.log(self.mu_log.INFO, "Jinja base directory taken from jinja configuration file >"
                                    + self.jinja_configuration_file
                                    + "<: "
                                    + self.jinja_base_directory, module)
                else:
                    self.mu_log.log(self.mu_log.INFO, "Jinja base directory setting not found in jinja configuration file."
                                    + " Using current directory")
                    self.jinja_base_directory = "."
                if "application" in data:
                    self.jinja_application = data["application"]
                    self.mu_log.log(self.mu_log.INFO, "Jinja application setting taken from jinja configuration file >"
                                    + self.jinja_configuration_file
                                    + "<: "
                                    + self.jinja_application, module)
                else:
                    self.mu_log.log(self.mu_log.INFO, "Jinja application setting not found. Using empty value", module)
                    self.jinja_application = None
                if "templates" in data:
                    self.jinja_templates = data["templates"]
                    self.mu_log.log(self.mu_log.INFO, "Jinja templates setting taken from jinja configuration file >"
                                    + self.jinja_configuration_file
                                    + "<: "
                                    + self.jinja_templates, module)
                else:
                    self.mu_log.log(self.mu_log.INFO, "Jinja templates setting not found. Using empty value", module)
                    self.jinja_templates = None

                self.jinja_template_directory = self.jinja_base_directory
                if self.jinja_application is not None:
                    self.jinja_template_directory += self.jinja_application
                if self.jinja_templates is not None:
                    self.jinja_template_directory += "/" + self.jinja_templates

                self.mu_log.log(self.mu_log.INFO, "Jinja template directory: " + self.jinja_template_directory, module)
                self.jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(self.jinja_template_directory))
                self.jinja_environment.filters["jsonify"] = json.dumps

        except FileNotFoundError:
            self.mu_log.log(self.mu_log.ERROR, "Could not find jinja configuration file: " + self.jinja_configuration_file
                            , module)
            return messages.message["jinja_config_file_not_found"]

        return result

    def build_api_load(self):
        module = "EDCLineage.build_api_load"
        try:
            self.template = self.jinja_environment.get_template(self.meta_type + ".json")
            self.mu_log.log(self.mu_log.DEBUG, "Found jinja template: " + self.meta_type + ".json", module)
        except jinja2.exceptions.TemplateNotFound:
            self.mu_log.log(self.mu_log.ERROR, "Could not find jinja template >" + self.meta_type + ".json<."
                            + " in directory >" + self.jinja_template_directory + "<."
                            , module)
            self.payload = {}
            return messages.message["jinja_template_not_found"], self.payload

        if self.meta_type == "physical_entity_association":
            build_result, self.payload = self.build_api_load_entity_association()
        elif self.meta_type == "physical_attribute_association":
            build_result, self.payload = self.build_api_load_attribute_association()
        else:
            build_result = messages.message["unknown_metadata_target"]
            self.payload = {}

        self.mu_log.log(self.mu_log.VERBOSE, "payload: " + self.payload, module)
        return build_result, self.payload

    def build_api_load_entity_association(self):
        """
        Loop through the list of source_target_entities
        """
        module = "EDCLineage.build_api_load_entity_association"
        build_result = messages.message["ok"]
        source_target_links = self.data["source_target_entity_links"]
        source_target_list = []
        update_entry_list = []

        template_updates = self.jinja_environment.get_template("physical_association_updates.jinja2")
        template_update_entry = self.jinja_environment.get_template("physical_association_update_entry.jinja2")
        template_new_sourcelinks = self.jinja_environment.get_template("physical_association_source_link.jinja2")
        target = ""
        for source_target_entity in source_target_links:
            self.mu_log.log(self.mu_log.DEBUG, "entity link from >" + source_target_entity["from"] + "< to >"
                            + source_target_entity["to"] + "<", module)
            find_result = self.generic.find_json(source_target_entity["from"], "physical_entity", "uid"
                                                 , log_prefix="from " + source_target_entity["from"] + " - ")
            if find_result["code"] != "OK":
                self.mu_log.log(self.mu_log.ERROR,
                                "The entity association contains a source UUID that could not be found in any entity JSON file."
                                ,module)
                build_result = messages.message["json_uuid_not_found"]
                return build_result, {}

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
                                "The entity association contains a target UUID that could not be found in any entity JSON file."
                                , module)
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
        module = "EDCLineage.build_api_load_attribute_association"
        build_result = messages.message["ok"]
        source_target_links = self.data["source_target_attribute_links"]
        source_target_list = []
        update_entry_list = []

        template_updates = self.jinja_environment.get_template("physical_association_updates.jinja2")
        template_update_entry = self.jinja_environment.get_template("physical_association_update_entry.jinja2")
        template_new_source_links = self.jinja_environment.get_template("physical_association_source_link.jinja2")

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
        module = "EDCLineage.send_metadata_to_edc"
        self.mu_log.log(self.mu_log.VERBOSE, "sending payload >" + str(self.payload) + "<.", module)
        start_time = time.time()
        self.edc_helper.initUrlAndSessionFromEDCSettings()

        self.mu_log.log(self.mu_log.DEBUG, "EDC base URL: " + self.settings.edc_url, module)
        url = self.settings.edc_url + "/access/1/catalog/data/objects"
        self.mu_log.log(self.mu_log.DEBUG, "Used URL >" + url + "<.", module)
        head = {'Content-Type': 'application/json'}
        self.mu_log.log(self.mu_log.VERBOSE, "Headers: " + str(head.items()), module)
        self.mu_log.log(self.mu_log.VERBOSE, "Proxies: " + str(self.proxies), module)
        if self.settings.edc_auth is None:
            self.mu_log.log(self.mu_log.WARNING
                            , "Auth not set. Add edc_auth to the edc.secrets file or set INFA_EDC_AUTH"
                            , module)
        # else:
        #    self.mu_log.log(self.mu_log.VERBOSE, "Auth: " + self.settings.auth)

        if suppress_edc_call:
            self.mu_log.log(self.mu_log.WARNING
                            , "'suppress_edc_call' is set to True in config.json. EDC call NOT exucuted", module)
            send_result = messages.message["ok"]
        else:
            response = self.edc_helper.session.patch(url, self.payload, timeout=20, headers=head, proxies=self.proxies)
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

