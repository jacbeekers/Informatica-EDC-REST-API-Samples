Module metadata_utilities.generic
=================================

Classes
-------

`Generic()`
:   Some generic utilities, e.g. reading the config.json

    ### Class variables

    `code_version`
    :

    `json_file`
    :

    `metaschema_version`
    :

    `mu_log`
    :

    `settings`
    :

    ### Methods

    `convert_list_into_string(self, list)`
    :

    `find_json(self, source_uuid, target_schema_type, property, log_prefix='')`
    :   find the JSON file that has the source_uuid in the value of the property.
        The JSON schema of the file must be 'target_schema_type'.

    `write_local_file(self, filename, to_write)`
    :