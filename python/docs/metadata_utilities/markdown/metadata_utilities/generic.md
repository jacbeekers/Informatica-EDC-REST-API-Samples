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

    `find_json(self, source_uuid, target_schema_type, property, log_prefix='')`
    :   find the JSON file that has the source_uuid in the value of the property.
        The JSON schema of the file must be 'target_schema_type'.

    `get_jinja_settings(self)`
    :   Get the Jinja settings from the provided jinja configuration file: jinja_config key in main config.json

    `get_jinja_template(self, template_name)`
    :

    `write_local_file(self, filename, to_write)`
    :