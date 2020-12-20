Module metadata_utilities.generic
=================================

Classes
-------

`Generic(settings, mu_log_ref)`
:   Some generic utilities, e.g. reading the config.json

    ### Class variables

    `code_version`
    :

    ### Methods

    `convert_list_into_string(self, list)`
    :

    `find_json(self, source_uuid, target_schema_type, property, log_prefix='', skip_file_list=None)`
    :   find the JSON file that has the source_uuid in the value of the property.
        The JSON schema of the file must be 'target_schema_type'.
        Params:
            source_uuid: the uuid for search for
            target_schema_type: which schema. Will filter on only those files that contain the specified entity type
            property: which property (key) in the file should contain the uuid
            log_prefix: text that will be added to any log messages. Useful to identify the related log entries

    `get_jinja_settings(self)`
    :   Get the Jinja settings from the provided jinja configuration file: jinja_config key in main config.json

    `get_jinja_template(self, template_name)`
    :

    `write_local_file(self, directory=None, filename='dummy', to_write='')`
    :