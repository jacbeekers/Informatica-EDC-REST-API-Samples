message = {
    "GEN_GROUP": {
        "code": "GEN"
        , "message": "Group for generic error or warning"
        , "level": "INFO"
    },
    "ok": {
        "code": "OK"
        , "message": "No errors encountered"
        , "level": "INFO"
    },
    "not_implemented": {
        "code": "MU-GEN-000"
        , "message": "Function not yet implemented. Please contact the development team and mention code 'MU-GEN-000'."
        , "level": "ERROR"
    },
    "not_found": {
        "code": "MU-GEN-001"
        , "message": "Could not find what we were looking for"
        , "level": "ERROR"
    },
    "os_error": {
        "code": "MU-GEN-002"
        , "message": "An OS error occurred"
        , "level": "ERROR"
    },
    "ignore": {
        "code": "MU-GEN-003"
        , "message": "Entry has been ignored"
        , "level": "DEBUG"
    },
    "undetermined": {
        "code": "MU-GEN-004"
        ,
        "message": "Undetermined result. This should not happen. Please contact the development team and mention code 'MU-GEN-004'."
        , "level": "ERROR"
    },
    "main_config_not_found": {
        "code": "MU-GEN-005"
        ,"message": "Main configuration file not found."
        ,"level": "FATAL"
    },
    "edc_config_not_found": {
        "code": "MU-GEN-006"
        ,"message": "EDC configuration file was provided, but could not be found. Check your main configuration file."
        ,"level": "FATAL"
    },
    "edc_secrets_not_found": {
        "code": "MU-GEN-007"
        ,"message": "EDC secrets file was provided, but could not be found. Check your configuration file."
        ,"level": "FATAL"
    },
    "azure_config_not_found": {
        "code": "MU-GEN-008"
        ,"message": "Azure configuration file was provided, but could not be found. Check your main configuration file."
        ,"level": "FATAL"
    },
    "log_config_not_found": {
        "code": "MU-GEN-009"
        ,"message": "Log configuration file was provided, but could not be found. Check your main configuration file."
        ,"level": "FATAL"
    },
    "unsupported_meta_version_edc_config": {
        "code": "MU-GEN-010"
        ,"message": "EDC configuration file contains meta_version that is not supported (yet)."
        ,"level": "ERROR"
    },
    "unsupported_meta_version_edc_secrets": {
        "code": "MU-GEN-011"
        ,"message": "EDC configuration file contains meta_version that is not supported (yet)."
        ,"level": "ERROR"
    },
    "main_config_issue": {
        "code": "MU-GEN-011"
        , "message": "There is an issue with the main configuration file."
        , "level": "FATAL"
    },
    "custom_attribute_file_not_found": {
        "code": "MU-GEN-012"
        , "message": "Custom attribute file not found."
        , "level": "ERROR"
    },
    "log_config_is_none": {
        "code": "MU-GEN-013"
        ,"message": "The log_config settings is None (empty)"
        , "level": "FATAL"
    },
    "no_data_provided_for_formulas": {
        "code": "MU-GEN-014"
        , "message": "No data provided for formulas"
        , "level": "ERROR"
    },
    "CONV_GROUP": {
        "code": "CONV"
        , "message": "Group for conversion and schema warnings and errors"
        , "level:": "INFO"
    },
    "meta_error": {
        "code": "MU-CONV-001"
        , "message": "JSON file does not contain a valid schema and/or schema version reference"
        , "level:": "ERROR"
    },
    "json_schema_error": {
        "code": "MU-CONV-002"
        , "message": "JSON schema error"
        , "level": "FATAL"
    },
    "json_validation_error": {
        "code": "MU-CONV-003"
        , "message": "JSON validation error"
        , "level": "FATAL"
    },
    "json_parse_error": {
        "code": "MU-CONV-004"
        , "message": "JSON parsing error"
        , "level": "FATAL"
    },
    "not_lineage": {
        "code": "MU-CONV-005"
        , "message": "JSON file is not meant for lineage and will be ignored"
        , "level": "WARNING"
    },
    "incorrect_meta_version": {
        "code": "MU-CONV-006"
        , "message": "JSON file meta-version does not match expected meta-version"
        , "level": "ERROR"
    },
    "jsonschema_validation_error": {
        "code": "MU-CONV-007"
        , "message": "JSON validation error against its schema"
        , "level": "ERROR"
    },
    "json_multiple_uuids_found": {
        "code": "MU-CONV-008"
        , "message": "Multiple UUIDs found, which is not allowed"
        , "level": "ERROR"
    },
    "json_uuid_not_found": {
        "code": "MU-CONV-009"
        , "message": "UUID could not be found"
        , "level": "ERROR"
    },
    "unknown_metadata_target": {
        "code": "MU-CONV-010"
        , "message": "Unknown metadata target type"
        , "level": "ERROR"
    },
    "invalid_lineage_output_type": {
        "code": "MU-CONV-011"
        , "message": "Invalid lineage output type specified"
        , "level": "ERROR"
    },
    "json_key_error": {
        "code": "MU-CONV-012"
        , "message": "JSON key could not be found in JSON file"
        , "level": "ERROR"
    },
    "missing_uid": {
        "code": "MU-CONV-013"
        , "message": "Missing UID key"
        , "level": "ERROR"
    },
    "schema_file_not_found": {
        "code": "MU-CONV-014"
        , "message": "Schema file could not be found"
        , "level": "ERROR"
    },
    "EDC_GROUP": {
        "code": "EDC"
        , "message": "Group for warnings and errors related to Informatica EDC interfacing"
        , "level:": "INFO"
    },
    "edc_error": {
        "code": "MU-EDC-001"
        , "message": "EDC reported an error (see above for more info)"
        , "level": "ERROR"
    },
    "invalid_api_response": {
        "code" : "MU-EDC-002"
        , "message": "EDC API did not return a JSON object"
        , "level": "ERROR"
    },
    "custom_attribute_not_found": {
        "code": "MU-EDC-003"
        , "message": "Custom Attribute could not be found."
        , "level": "ERROR"
    },
    "custom_attribute_already_exists": {
        "code": "MU-EDC-004"
        , "message": "Custom Attribute already exists."
        , "level": "ERROR"
    },
    "edc_status_not_200": {
        "code": "MU-EDC-005"
        , "message": "EDC did not return status=200."
        , "level": "ERROR"
    },
    "edc_status_401": {
        "code": "MU-EDC-006"
        , "message": "EDC returned 401: unauthorized access. Please check the encoded Authorization value in edc.secrets."
        , "level": "ERROR"
    },
    "edc_error_creating_custom_attribute": {
        "code": "MU-EDC-007"
        , "message": "An error occurred creating the custom attribute"
        , "level": "ERROR"
    },
    "edc_custom_attribute_already_exists": {
        "code": "MU-EDC-008"
        , "message": "Custom Attribute already exists"
        , "level": "ERROR"
    },
    "no_custom_attribute_provided": {
        "code": "MU-EDC-009"
        , "message": "No Custom Attribute information provided"
        , "level": "ERROR"
    },
    "edc_connection_validation_failed": {
        "code": "MU-EDC-010"
        , "message": "EDC connection validation failed."
        , "level": "ERROR"
    },
    "edc_connection_failed": {
        "code": "MU-EDC-011"
        , "message": "Connection to EDC failed."
        , "level": "ERROR"
    },
    "MDL_GROUP": {
        "code": "MDL"
        , "message": "Group for warnings and errors related to the Metadata Lake"
        , "level:": "INFO"
    },
    "JINJA_GROUP": {
        "code": "JIN"
        , "message": "Group for warnings and errors related to the Jinja templating"
        , "level:": "INFO"
    },
    "jinja_config_file_not_found": {
        "code": "MU-JIN-001"
        , "message": "Could not find Jinja configuration file"
        , "level": "ERROR"
    },
    "jinja_template_not_found": {
        "code": "MU-JIN-002"
        , "message": "Jinja template not found. Check the Jinja directory settings"
        , "level": "ERROR"
    },
    "jinja_template_name_not_provided": {
        "code": "MU-JIN-003"
        , "message": "No Jinja template name was provided."
        , "level": "ERROR"
    },
    "INTERNAL_GROUP": {
        "code": "INT"
        , "message": "Group for internal warnings and errors, i.e. there is a code issue (aka Bug)"
        , "level:": "INFO"
    },
    "invalid_http_method": {
        "code": "INT-001"
        , "message": "Internal error in call to requests. An invalid / unsupported method was used."
        , "level": "ERROR"
    }
}
