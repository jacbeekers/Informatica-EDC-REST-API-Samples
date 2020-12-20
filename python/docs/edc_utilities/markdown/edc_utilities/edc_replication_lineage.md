Module edc_utilities.edc_replication_lineage
============================================
Created on December 19, 2020 to work with files and fields
Based on https://github.com/Informatica-EIC/REST-API-Samples/blob/master/python/dbSchemaReplicationLineage.py
Created on Jun 26, 2018

@author: dwrigley
***************************************************************************************
Folder replication custom lineage generator

process:-
    scenario:  the files in 2 different folders
    (perhaps in different resources) are replicated
    in EDC - we have no way to automatically know that there is lineage
    between the folder contents (files & fields)
    this utility will generate the custom lineage import to create the links

    given two folders - leftSchema and rightSchema
    find the 2 folder objects in the catalog (GET /2/catalog/data/objects)

    for each schema
        execute /2/catalog/data/relationships (2 levels folder->file->column)
            for each file & field - store the id & name (names converted to
            lower-case for case-insensitive match)

    for the stored objects (files/fields) left side...
        find the same file/field in the right side
        if found - write a custom lineage link to csv

    Note:  the custom lineage format used is:-
        Association,From Connection,To Connection,From Object,To Object

        where:  From Connection and To Connection will be empty
                Association will be either core.DirectionalDataFlow
                or core.DataSetDataFlow
                the From and To Object will be the full object id

        when importing - there is no need for auto connection assignment,
        since the full id's are provided this happens automatically
        this is possible using v10.2.0 with a patch,
        and works native in v10.2.1+

Classes
-------

`EDCReplicationLineage(configuration_file='resources/config.json')`
:   

    ### Methods

    `get_schema_contents(self, schema_name, schema_type, resource_name, container_name)`
    :   given a schema name, schema class type (e.g. hanadb is different)
        and resource name, find the schema object
        then
            execute a relationships call to get the schema tables & columns
            (parent/child links)
            note:  some models separate primary key columns from regular columns
            note:  some models have different relationships (e.g. sap hana db)
        
        returns a dictionary of all tables & columns for the schema & the id of
        the schema object
        key=table  val=tableid
        key=table.column  val=columnid

    `main(self)`
    :   initialise the csv file(s) to write
        call get_schema_contents for both left and right schema objects
        match the tables/columns from the left schema to the right
        when matched
            write a lineage link - table and column level
        
        Note:  this script generates the newer lineage format using complete
               object id's and relationship types
               connection assignment will not be necessary
               works with v10.2.1+