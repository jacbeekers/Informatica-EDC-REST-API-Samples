import json

import jsonschema

from metadata_utilities import messages, generic_settings, mu_logging


class CheckSchema:
    """
    Checks the JSON schema of a given JSON file
    """
    code_version = "0.2.0"
    # TODO: Get the info from the file and check if that schema version exists
    metaschema_version = generic_settings.GenericSettings().meta_version

    def __init__(self):
        self.json_file = "not provided"
        self.json_data = ""
        self.meta_type = "unknown"
        self.meta_version = "unknown"
        self.schema_file = "unknown"
        self.mu_log = mu_logging.MULogging()

    def check_schema(self, data):
        """
        Checks the JSON to determine which JSON schema is used and which version
        """
        module = "check_schema"
        self.mu_log.log(self.mu_log.DEBUG, "expected meta_version is >" + self.metaschema_version + "<", module)
        self.json_data = data

        try:
            self.meta_type = data["meta"]
            self.meta_version = data["meta_version"]
            self.mu_log.log(self.mu_log.DEBUG
                            , "schema is >" + self.meta_type + "<, version >"
                            + self.meta_version + "<", module)
        except KeyError as e:
            self.mu_log.log(self.mu_log.DEBUG,
                            "Key error. meta and meta_version must be in JSON file. That is not the case with "
                            + self.json_file, module)
            return messages.message["meta_error"]
        except jsonschema.exceptions.SchemaError as e:
            self.mu_log.log(self.mu_log.FATAL, "Schema error: " + e.message, module)
            return messages.message["json_schema_error"]
        except jsonschema.exceptions.ValidationError as e:
            self.mu_log.log(self.mu_log.FATAL, "Validation error: " + e.message, module)
            return messages.message["json_validation_error"]
        except json.decoder.JSONDecodeError as e:
            self.mu_log.log(self.mu_log.FATAL, "Error parsing JSON:" + e.msg, module)
            return messages.message["json_parse_error"]

        if self.meta_version == generic_settings.GenericSettings().meta_version:
            self.mu_log.log(self.mu_log.INFO, "file meta version matches expected schema version", module)
            schema_directory = generic_settings.GenericSettings().schema_directory
            self.schema_file = schema_directory + self.meta_type + ".json"
            with open(self.schema_file) as f:
                schema = json.load(f)
                try:
                    jsonschema.validate(data, schema)
                    self.mu_log.log(self.mu_log.INFO, "JSON file validated successfully against schema", module)
                except jsonschema.exceptions.SchemaError as e:
                    self.mu_log.log(self.mu_log.FATAL, "A schema error occurred during validation", module)
                    return messages.message["jsonschema_validation_error"]
                except jsonschema.exceptions.ValidationError as e:
                    self.mu_log.log(self.mu_log.ERROR, "A validation error occurred", module)
                    return messages.message["jsonschema_validation_error"]
        else:
            self.mu_log.log(self.mu_log.DEBUG, "File meta version does not match expected schema version", module)
            return messages.message["incorrect_meta_version"]

        return messages.message["ok"]
