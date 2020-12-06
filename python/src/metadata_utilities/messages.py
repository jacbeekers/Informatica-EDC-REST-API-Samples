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
    "MDL_GROUP": {
        "code": "MDL"
        , "message": "Group for warnings and errors related to the Metadata Lake"
        , "level:": "INFO"
    },

}
