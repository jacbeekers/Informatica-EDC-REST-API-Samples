Module edc_utilities.edc_lineage
================================

Classes
-------

`EDCLineage(settings, mu_log_ref)`
:   EDLineage: Call Informatica EDC APIs to add lineage information for existing objects

    ### Class variables

    `code_version`
    :

    `patch_payload_file`
    :

    `this_run`
    :

    `this_run_dir`
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

    `encode_id(self, edc_attribute_id, tilde=True)`
    :   Encode an ID to be safe. Return String.
        Thankfully copied from
            https://github.com/Informatica-EIC/REST-API-Samples/blob/c97beb76724349db95abde5801d443ace04d51dd/python/Base/InformaticaAPI.py
        Parameters
        ----------
        edc_attribute_id : String
            ID of object
        tilde : Boolean, optional (default=True)
            Whether to encode with a tilde or percent sign.

    `find_to_entity_and_attribute(self, transformation)`
    :

    `generate_lineage(self, output_type, metadata_type, data, generic_settings)`
    :

    `get_custom_attribute(self, look_for_attribute_name)`
    :   Based on Informatica's sample code: listCustomAttributes.py

    `get_data_references_before_v_0_3(self)`
    :

    `get_data_references_v0_3(self)`
    :

    `get_edc_data_references(self)`
    :

    `get_list_of_from_attributes(self, attribute_list)`
    :

    `send_metadata_to_edc(self, suppress_edc_call=False, method='PATCH', uri='/access/1/catalog/data/objects', etag=None, parameters=None, payload=None)`
    :

    `update_object_attributes(self, entity_type, data, settings)`
    :   Update formulas for to_attributes
        Given the time pressure, it was advised NOT the change the code that builds the lineage.
        TODO: Revisit code to not do things both in update_object_attributes and build_api_load_attribute_association