Module metadata_utilities.load_json_metadata
============================================

Classes
-------

`ConvertJSONtoEDCLineage(configuration_file='resources/config.json')`
:   Converts JSON file to a JSON payload that can be send to Informatica EDC using its APIs

    ### Class variables

    `code_version`
    :

    ### Methods

    `create_metafile(self, location, filename, attributes)`
    :   A metafile is created for Informatica EDC to scan. This way no real data is needed.

    `find_entity_in_source_target_links(self, source_uuid, target_schema_type='physical_entity_association', log_prefix='')`
    :   find_entity_in_source_target_links
        Determines whether an entity is used as source or target (or both) in the current run
        Based on the outcome, the metafile can be created in the location as determined by the config file

    `generate_file_structure(self)`
    :   Generate the metadata file for the data. The result is a file with only a header. No real data is needed.

    `generate_transformations(self)`
    :   generate a transformation file for each encountered transformation in the attribute_association json

    `main(self, metafiles_only=False)`
    :   Main module to process JSON files that are stored at the location stated in the provided configuration file
        configuration_file: a relative or absolute path to the configuration file. Default is resources/config.json

    `process_files(self)`
    :   Process files in the configued json directory (check config.json)
        For each file: Validate its schema and generate the metadata definition file or lineage file
            (depends on the meta_type of the file found)

    `process_lineage_request(self, metafiles_only=False)`
    :

    `process_physical_entity_and_attribute(self)`
    :   Generate metadata files to be parsed by EDC

    `send_metadata_to_metadata_lake(self)`
    :