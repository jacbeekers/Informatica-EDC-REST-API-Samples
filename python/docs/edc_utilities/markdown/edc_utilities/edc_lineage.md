Module edc_utilities.edc_lineage
================================

Classes
-------

`EDCLineage(settings, mu_log_ref)`
:   EDLineage: Call Informatica EDC APIs to add lineage information for existing objects

    ### Class variables

    `code_version`
    :

    `total`
    :

    ### Methods

    `build_api_load(self)`
    :

    `build_api_load_attribute_association(self)`
    :   Loop through the list of source_target_attributes

    `build_api_load_entity_association(self)`
    :   Loop through the list of source_target_entities

    `generate_lineage(self, output_type, metadata_type, data, generic_settings)`
    :

    `get_edc_data_references(self)`
    :

    `get_jinja_settings(self, generic_settings)`
    :   Get the Jinja settings from the provided jinja configuration file: jinja_config key in main config.json

    `send_metadata_to_edc(self, suppress_edc_call=False)`
    :