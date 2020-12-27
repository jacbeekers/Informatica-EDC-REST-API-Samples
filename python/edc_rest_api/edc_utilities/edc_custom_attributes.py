from src.metadata_utilities import messages
from src.metadata_utilities import generic_settings, mu_logging, generic
import logging
import time
from src.edc_utilities import edc_session_helper
import requests
import time
import json
import urllib3
urllib3.disable_warnings()


class EDCCustomAttribute:
    """
    Class to get, add, update, delete custom attributes
    """

    def __init__(self, settings_ref=None, configuration_file=None):
        """
        Instance initialization
            settings_ref is a reference to an existing generic_settings object. If None, the settings will be collected
            from the configuration_file mentioned in the configuration_file argument
            If both settings_ref and configuration_file are set, the configuration_file argument will be ignored.
        """
        module = __name__ + ".__init__"
        self.timeout = 10

        self.settings = None
        self.settings_found = False
        self.mu_log = None

        if settings_ref is None:
            if configuration_file is None:
                current_configuration_file = "resources/config.json"
            else:
                current_configuration_file = configuration_file
            # print(module, "settings_ref is None. Getting them myself.")
            self.settings = generic_settings.GenericSettings(configuration_file=current_configuration_file)
            result = self.settings.get_config()
            if result != messages.message["ok"]:
                self.settings_found = False
                print(module, "Could not get main config. Error:", result["code"])
            else:
                self.mu_log = self.settings.mu_log
                self.mu_log.log(self.mu_log.DEBUG, "Generic settings loaded.", module)
                self.settings_found = True
        else:
            self.settings = settings_ref
            self.settings_found = True

        if self.mu_log is None:
            self.mu_log = mu_logging.MULogging("resources/log_config.json")
            self.mu_log.setup_logger(logging.DEBUG, logging.INFO)
            self.mu_log.log(self.mu_log.DEBUG, "mu_log was None. Logger has been setup now.", module)
            self.settings.mu_log = self.mu_log

        self.generic = generic.Generic(self.settings, self.mu_log)
        self.generic.get_jinja_settings()
        self.edc_helper = edc_session_helper.EDCSession(self.settings)
        # edc_helper already initializes a session
        self.session = self.edc_helper.session
        # self.mu_log.log(self.mu_log.DEBUG, "headers: " + str(self.session.headers.items()), module)
        self.retries = 0
        self.max_retries = 3

    def reconnect(self):
        self.session = self.edc_helper.init_edc_session()
        self.retries += 1

    def get_custom_attribute(self, name="dummy", expect_to_exist=True):
        """
        Get the EDC attribute
        This is an expensive operation, so we should cache it
        """
        module = __name__+".get_custom_attribute"
        start_time = time.time()
        url = self.settings.edc_url + "/access/2/catalog/data/objects"
        total = 100000
        offset = 0
        page = 0
        page_size = 500
        timeout = self.timeout

        attribute_count = 0
        custom_attribute_count = 0
        resp = None

        found = False
        from_scratch = True
        self.mu_log.log(self.mu_log.DEBUG, "URL used: " + url, module)

        items_found = True
        while offset < total and self.retries < self.max_retries and items_found:
            if from_scratch:
                offset = 0
                page = 0
                from_scratch = False

            page += 1
            parameters = {"offset": offset, "pageSize": page_size}
            self.mu_log.log(self.mu_log.DEBUG, "Getting page#" + str(page), module)

            # execute catalog rest call, for a page of results
            if self.settings.suppress_edc_call:
                self.mu_log.log(self.mu_log.WARNING, "suppress_edc_call is True. Skipping EDC call...", module)
                status = 200
                result_json = json.dumps({}, indent=4)
            else:
                try:
                    resp = self.session.get(url, params=parameters, timeout=timeout, headers=self.session.headers)
                    status = resp.status_code
                    result_json = resp.json()
                    # store the total, so we know when the last page of results is read
                    total = result_json["metadata"]["totalCount"]
                except requests.exceptions.RequestException as e:
                    print(module, str(e))
                    self.mu_log.log(self.mu_log.ERROR, "An error occurred: " + str(e), module)
                    self.mu_log.log(self.mu_log.WARNING, "retry#" + str(self.retries+1), module)
                    self.reconnect()
                    from_scratch=True
                    continue

            # no execption rasied - so we can check the status/return-code
            if status != 200:
                self.mu_log.log(self.mu_log.ERROR, "EDC returned: " + str(status), module)
                return messages.message["edc_status_not_200"]
            else:
                self.mu_log.log(self.mu_log.DEBUG, "EDC returned 200 = ok.", module)

            # self.mu_log.log(self.mu_log.INFO, "Total number of items: " + str(total), module)
            # for next iteration
            offset += page_size

            # for each attribute found...
            attrId = ""
            if "items" not in result_json:
                self.mu_log.log(self.mu_log.INFO, "No items in JSON response.", module)
                items_found = False
            else:
                items_found = True
                for attrDef in result_json["items"]:
                    attribute_count += 1
                    attrId = attrDef["id"]
                    # self.mu_log.log(self.mu_log.VERBOSE, "Found id: " + attrId, module)
                    if "name" in attrDef:
                        attrName = attrDef["name"]
                    else:
                        attrName = "<undefined>"
                    if "dataTypeId" in attrDef:
                        dataType = attrDef["dataTypeId"]
                    if attrId.startswith("com.infa.appmodels.ldm.*"):
                        custom_attribute_count += 1
                    # self.mu_log.log(self.mu_log.VERBOSE, "Found Custom Attribute #" + str(custom_attribute_count)
                    #        + ", name: " + attrName + " id: " + attrId, module)
                    if attrName == name:
                        self.mu_log.log(self.mu_log.INFO, "Found the attribute we were looking for!", module)
                        found = True
                    # else:
                        # self.mu_log.log(self.mu_log.VERBOSE, "This is not the attribute we are looking for.", module)

        end_time = time.time()
        self.mu_log.log(self.mu_log.INFO, "Processing time: " + str(end_time - start_time), module)

        if self.settings.suppress_edc_call and expect_to_exist:
            found = True

        if found:
            return messages.message["ok"]
        else:
            return messages.message["custom_attribute_not_found"]

    def create_custom_attribute(self, custom_attribute_values=None):
        """
        Create new custom attribute
        Will fail if attribute already exists
        """
        module = __name__ + ".create_custom_attribute"
        start_time = time.time()

        if custom_attribute_values is None:
            result = messages.message["no_custom_attribute_provided"]
            return result

        name = custom_attribute_values["items"][0]["name"]
        # result, the_template = self.generic.get_jinja_template("edc_create_attributes.jinja2")
        # custom_attribute_json = self.fill_in_jinja_template_custom_attributes(the_template, custom_attribute_values)
        custom_attribute_json = json.dumps(custom_attribute_values, indent=4)
        self.mu_log.log(self.mu_log.DEBUG, "JSON for custom attribute >" + name + "< is: " + str(custom_attribute_json)
                        ,module)

        url = self.settings.edc_url + "/access/2/catalog/models/attributes"
        resp = None
        result = messages.message["undetermined"]

        try:
            if self.settings.suppress_edc_call:
                self.mu_log.log(self.mu_log.WARNING, "suppress_edc_call is True. Skipping EDC call...", module)
                status = 200
            else:
                resp = self.session.post(url, custom_attribute_json, timeout=self.timeout, headers=self.session.headers)
                status = resp.status_code
            if status == 200:
                # TODO: Check response body on "metadata": { "totalCount": 1 }
                self.mu_log.log(self.mu_log.INFO, "Custom Attribute successfully created.", module)
                result = messages.message["ok"]
            elif resp.status_code == 400:
                if "already exists" in str(resp.content) and name in str(resp.content):
                    self.mu_log.log(self.mu_log.ERROR, "Custom attribute >" + name + "< already exists.", module)
                    result = messages.message["edc_custom_attribute_already_exists"]
                else:
                    self.mu_log.log(self.mu_log.ERROR, "HTTP 400 occurred, but not because attribute already exists."
                                    , module)
                    result = messages.message["edc_error_creating_custom_attribute"]
            else:
                self.mu_log.log(self.mu_log.ERROR,
                                "Error creating custom attribute. HTTP Response code: " + str(resp.status_code)
                                , module)
                result = messages.message["edc_error_creating_custom_attribute"]
        except requests.exceptions.RequestException as e:
            self.mu_log.log(self.mu_log.ERROR, "An error occurred: " + str(e), module)
            result = messages.message["edc_error_creating_custom_attribute"]

        end_time = time.time()
        self.mu_log.log(self.mu_log.INFO, "Processing time: " + str(end_time - start_time), module)

        return result

    def update_custom_attribute(self, name="dummy"):
        """
        Update a give custom attribute
        """
        module = __name__ + ".update_custom_attribute"

        if self.settings.suppress_edc_call:
            self.mu_log.log(self.mu_log.WARNING, "suppress_edc_call is True. Skipping EDC call...", module)
            status = 200
            result = messages.message["ok"]
        else:
            # TODO: Call EDC to update the custom attribute
            result = messages.message["not_implemented"]

        return result

    def delete_custom_attribute(self, name="dummy", ignore_already_gone=True):
        """
        Delete a give custom attribute
        """
        module = __name__ + ".delete_custom_attribute"

        if self.settings.suppress_edc_call:
            self.mu_log.log(self.mu_log.WARNING, "suppress_edc_call is True. Skipping EDC call...", module)
            status = 200
            result = messages.message["ok"]
        else:
            # TODO: Call EDC to remove the custom attribute
            result = messages.message["not_implemented"]

        return result

    def fill_in_jinja_template_custom_attributes(self
                                                 ,the_template
                                                 ,custom_attribute_values
                                                 ):
        """
        the_template must be a Template object as retrieved through get_jinja_template
        """

        return the_template.render(allowed_classes=custom_attribute_values["classes_list"]
                                        ,attribute_description=custom_attribute_values["description"]
                                        ,attribute_name=custom_attribute_values["attribute_name"]
                                        ,type_allowed_resources=custom_attribute_values["assignment_type"]
                                        ,attribute_allowed_resources=custom_attribute_values["allowed_resources"]
                                   )
