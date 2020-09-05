message = {
    "ok": {
        "code": "OK"
        , "message": "No errors encountered"
        , "level": "INFO"
    },
    "not_implemented": {
        "code": "MU-CONV-000"
        , "message": "Function not yet implemented. Please ontact the development team and mention code 'MU-CONV-000'."
        , "level": "ERROR"
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
        "code": "MU-CONV-002"
        , "message": "JSON parsing error"
        , "level": "FATAL"
    },
    "not_lineage": {
        "code": "MU-CONV-003"
        , "message": "JSON file is not meant for lineage and will be ignored"
        , "level": "WARNING"
    },
    "incorrect_meta_version": {
        "code": "MU-CONV-004"
        , "message": "JSON file meta-version does not match expected meta-version"
        , "level": "ERROR"
    },
    "jsonschema_validation_error": {
        "code": "MU-CONV-005"
        , "message": "JSON validation error against its schema"
        , "level": "ERROR"
    }

}
