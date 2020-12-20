"""
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
"""

import argparse
import csv
import json
import logging
import time

import urllib3, requests

from src.edc_utilities import edc_session_helper
from src.edc_utilities import edcutils
from src.metadata_utilities import generic_settings
from src.metadata_utilities import mu_logging


class EDCReplicationLineage:
    # disable ssl cert warnings, when using self-signed certificate
    urllib3.disable_warnings()

    def __init__(self, configuration_file="resources/config.json"):
        module = __name__ + ".__init__"
        self.settings = generic_settings.GenericSettings(configuration_file)
        self.settings.get_config()
        # set edc helper session + variables (easy/re-useable connection to edc api)
        self.edc_helper = edc_session_helper.EDCSession(self.settings)
        self.mu_log = mu_logging.MULogging("resources/log_config.json")
        self.mu_log.setup_logger(logging.DEBUG, logging.INFO)
        self.mu_log.log(self.mu_log.DEBUG, "mu_log was None. Logger has been setup now.", module)
        self.settings.mu_log = self.mu_log

    def get_schema_contents(self, schema_name, schema_type, resource_name, container_name):
        """
        given a schema name, schema class type (e.g. hanadb is different)
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
        """
        print("\tget_schema_contents for:" + schema_name + " resource=" + resource_name)
        # schema_dict returned  key=TABLE.COLUMN value=column id
        schema_dict = {}
        table_names = {}

        # url = catalogServer + "/access/2/catalog/data/objects"
        # within a resource:
        # - core.classType = com.infa.ldm.file.Folder is e.g. ResourceName://FileServer/foldername/foldername
        # - core.classType = core.Resource with core.resourceName = the name of the resource

        url = self.edc_helper.baseUrl + "/access/2/catalog/data/objects"
        query = (f'+core.resourceName:"{resource_name}"'
                 + f' +core.classType:"{schema_type}"'
        #         + f' +core.name:"{schema_name}"'
                 )
        parameters = {"q": query, "offset": 0, "pageSize": 1000}
        print("\tquery=" + query)

        schema_id = None
        table_count = 0
        column_count = 0
        # make the call to find the schema object
        try:
            response = self.edc_helper.session.get(url, params=parameters)
            print(f"session get finished: {response.status_code}")
            rc = response.status_code
            if rc != 200:
                print("error reading object: rc=" + str(rc) + " response:" + str(response.json))
                if rc == 401:
                    print(
                        "\t401:Possible Missing/bad credentials"
                    )
                    print(str(response))
                return None, None
        except urllib3.exceptions.NewConnectionError or requests.exceptions.ConnectionError:
            print(f"Exception during get for url {url} with params {parameters}")
            response = None
            return None, None

        # get the total # of objects returned (first part of the json resultset)
        total_objects = response.json()["metadata"]["totalCount"]
        print("\tobjects returned: " + str(total_objects))

        for item in response.json()["items"]:
            schema_id = item["id"]
            schema_name = edcutils.get_fact_value(item=item, attribute_name="core.name")
            # get the tables & columns
            print("\tfound schema: " + schema_name + " id=" + schema_id)

            lineage_url = self.edc_helper.baseUrl + "/access/2/catalog/data/relationships"
            lineage_parameters = {
                "seed": schema_id,
                "association": "core.ParentChild",
                "depth": "2",
                "direction": "OUT",
                "includeAttribute": {"core.name", "core.classType"},
                "includeTerms": "false",
                "removeDuplicateAggregateLinks": "false",
            }
            print(
                "\tGET child relations for schema: " + lineage_url + " parms=" + str(lineage_parameters)
            )
            # get using uid/pwd
            lineage_resp = self.edc_helper.session.get(
                lineage_url,
                params=lineage_parameters,
            )
            lineage_status = lineage_resp.status_code
            print("\tlineage resp=" + str(lineage_status))
            if lineage_status != 200:
                print(
                    f"error getting schema contents (tables) rc={rc}"
                    f" response:{response.json}"
                )
                if rc == 401:
                    print(
                        "\t401:Possible missing/bad credentials"
                    )
                    print(str(response))
                return None, None

            if lineage_resp.text.startswith("{items:"):
                # bug (10.2.0 & 10.2.1) - the items collection should be "items"
                lineage_json = lineage_resp.text.replace("items", '"items"', 1)
            else:
                lineage_json = lineage_resp.text
            # relations_json = json.loads(lineage_json.replace('items', '"items"'))
            relations_json = json.loads(lineage_json)
            # print(len(relations_json))

            for lineage_item in relations_json["items"]:
                print('***NEW***\n\tlineage_item: ' + str(lineage_item))
                in_id = lineage_item.get("inId")
                out_id = lineage_item.get("outId")

                print('\t\tin_id===' + in_id + "\n\t\tout_id=" + out_id)
                # print(edcutils.getFactValue(lineage_item["inEmbedded"], "core.name"))
                association_id = lineage_item.get("associationId")
                print("\t\tassoc=" + association_id)
                # if association_id=='com.infa.ldm.relational.SchemaTable':
                if association_id.endswith(".DelimitedFileField") and "inEmbedded" in lineage_item:
                    # note - custom lineage does not need table and column
                    # count the tables & store table names
                    table_count += 1
                    # table_name = in_id.split('/')[-1]
                    #table_name = edcutils.get_fact_value(
                    #    lineage_item["inEmbedded"], "core.name"
                    #).lower()
                    # print("\t\tFilename: " + table_name)
                    out_id = out_id.split("/")[-1]
                    print("\t\tFilename: " + out_id)
                    # store the table name (for lookup when processing the columns)
                    # key=id, val=name
                    table_names[in_id] = out_id
                    schema_dict[out_id] = in_id
                # if association_id=='com.infa.ldm.relational.TableColumn':
                if (association_id.endswith(".DelimitedFileField") or association_id.endswith(".TablePrimaryKeyColumn")) \
                        and "inEmbedded" in lineage_item:
                    # column_name = in_id.split('/')[-1]
                    column_count += 1
                    column_name = edcutils.get_fact_value(
                        lineage_item["inEmbedded"], "core.name"
                    ).lower()
                    print("\t\t\tField name: " + column_name)
                    table_name = table_names[in_id].lower()
                    print("\t\tField=" + table_name + "." + column_name)
                    schema_dict[table_name + "." + column_name] = in_id

        print(
            "\tgetSchema: returning "
            + str(column_count)
            + " fields, in "
            + str(table_count)
            + " files"
        )
        return schema_dict, schema_id

    def main(self):
        """
        initialise the csv file(s) to write
        call get_schema_contents for both left and right schema objects
        match the tables/columns from the left schema to the right
        when matched
            write a lineage link - table and column level

        Note:  this script generates the newer lineage format using complete
               object id's and relationship types
               connection assignment will not be necessary
               works with v10.2.1+

        """
        module = __name__ + ".main"
        # define script command-line parameters (in global scope for gooey/wooey)
        parser = argparse.ArgumentParser(parents=[self.edc_helper.argparser])
        # add args specific to this utility (left/right resource, schema, classtype...)
        parser.add_argument(
            "-lr", "--leftresource", required=False, help="name of the left resource to find objects"
        )
        parser.add_argument(
            "-ls", "--leftschema", required=False, help="name of the left schema object"
        )
        parser.add_argument(
            "-lc", "--leftcontainer", required=False, help="name of the left container object"
        )
        parser.add_argument(
            "-lt", "--lefttype", required=False,
            help="class type for the schema level object"
        )
        parser.add_argument(
            "-rr", "--rightresource", required=False, help="name of the right resource to find objects"
        )
        parser.add_argument(
            "-rs", "--rightschema", required=False, help="name of the right schema object"
        )
        parser.add_argument(
            "-rc", "--rightcontainer", required=False, help="name of the right container object"
        )
        parser.add_argument(
            "-rt", "--righttype", required=False,
            help="class type for the right schema level object"
        )
        parser.add_argument(
            "-p", "--csvprefix", required=False, default="lineage_",
            help="prefix to use when creating the output csv file"
        )
        parser.add_argument(
            "-r", "--righttableprefix", required=False, default="", help="table prefix for right datasets"
        )
        parser.add_argument(
            "-o",
            "--outDir",
            required=False,
            help=(
                "output folder to write results - default = ./out "
                " - will create folder if it does not exist"
            ),
        )

        args = args, unknown = parser.parse_known_args()
        # setup edc session and catalog url - with auth in the session header,
        # by using system vars or command-line args
        self.edc_helper.init_edc_session()

        print("from settings:", self.settings.edc_config_data)
        print(f"command-line args parsed = {args} ")

        start_time = time.time()

        # Command line arguments have a higher priority
        left_resource = args.leftresource
        left_schema = args.leftschema
        left_container = args.leftcontainer
        left_type = args.lefttype
        right_resource = args.rightresource
        right_schema = args.rightschema
        right_container = args.rightcontainer
        right_type = args.righttype
        output_folder = args.outDir
        output_file_prefix = args.csvprefix
        right_table_prefix = args.righttableprefix

        # if not provided, use settings from config files
        # note: not checking. If you want to use it, make sure the edc_config contains the necessary keys
        if left_resource is None:
            left_resource = self.settings.edc_config_data["edc_source_resource_name"]
        left_resource = left_resource.split(":")[0]
        if left_schema is None:
            left_schema = self.settings.edc_config_data["edc_source_datasource"]
        if left_container is None:
            left_container = self.settings.edc_config_data["edc_source_container"]
        if left_type is None:
            left_type = self.settings.edc_config_data["edc_source_type"]
        if right_resource is None:
            right_resource = self.settings.edc_config_data["edc_target_resource_name"]
        right_resource = right_resource.split(":")[0]
        if right_schema is None:
            right_schema = self.settings.edc_config_data["edc_target_datasource"]
        if right_container is None:
            right_container = self.settings.edc_config_data["edc_target_container"]
        if right_type is None:
            right_type = self.settings.edc_config_data["edc_target_type"]

        if output_folder is None:
            output_folder = self.settings.output_directory

        if left_type is None:
            # left_type = "com.infa.ldm.relational.Schema"
            left_type = "com.infa.ldm.file.delimited.DelimitedFile"
        if right_type is None:
            # right_type = "com.infa.ldm.relational.Schema"
            right_type = "com.infa.ldm.file.delimited.DelimitedFile"

        print("dbSchemaReplicationLineage:start")
        print(f"Catalog={self.edc_helper.baseUrl}")
        print(f"left:  resource={left_resource}")
        print(f"left:    schema={left_schema}")
        print(f"left: container={left_container}")
        print(f"left:      type={left_type}")
        print(f"right:  resource={right_resource}")
        print(f"right:    schema={right_schema}")
        print(f"right: container={right_container}")
        print(f"right:      type={right_type}")
        print(f"output folder: {output_folder}")
        print(f"output file prefix: {output_file_prefix}")
        print(f"right table prefix: {right_table_prefix}")

        # initialize csv output file
        column_header = [
            "Association",
            "From Connection",
            "To Connection",
            "From Object",
            "To Object",
        ]

        # set the csv fileName
        csv_file_name = output_folder \
                        + output_file_prefix \
                        + "_" + left_container.replace("/","_").lower()\
                        + "_" + right_container.replace("/","_").lower() \
                        + ".csv"

        print("initializing file: " + csv_file_name)
        f_csv_file = open(csv_file_name, "w", newline="", encoding="utf-8")
        col_writer = csv.writer(f_csv_file)
        col_writer.writerow(column_header)

        # get the objects from the left schema into memory
        print(
            f"get left schema: name={left_schema}"
            f" resource={left_resource}"
            f" container={left_container}"
            f" type={left_type}"
        )
        left_objects, left_schema_id = self.get_schema_contents(
            left_schema, left_type, left_resource, left_container
        )

        # get the objects from the right schema into memory
        print(
            f"get right schema: name={right_schema}"
            f" resource={right_resource}"
            f" container={right_container}"
            f" type={right_type}"
        )
        right_objects, right_schema_id = self.get_schema_contents(
            right_schema, right_type, right_resource, right_container
        )

        matches = 0
        missing = 0

        if len(left_objects) > 0 and len(right_objects) > 0:
            # iterate over all left objects - looking for matching right ones
            print("\nprocessing: " + str(len(left_objects)) + " objects (left side)")
            first_find =  True
            for left_name, left_val in left_objects.items():
                # if the target is using a prefix - add it to left_name
                if len(right_table_prefix) > 0:
                    left_name = right_table_prefix.lower() + left_name

                print("checking for left key=" + left_name, " in right_object keys: ", right_objects.keys())
                if left_name in right_objects.keys():
                    # match
                    right_val = right_objects.get(left_name)
                    print("right_val=", right_val)
                    matches += 1
                    if first_find:
                        # create the lineage file
                        col_writer.writerow(
                            ["core.DataSourceDataFlow", "", "", left_schema_id.rsplit("/", 1)[0]
                                , right_schema_id.rsplit("/", 1)[0]]
                        )
                        col_writer.writerow(
                            ["core.DataSetDataFlow"
                                , ""
                                , ""
                                , left_schema_id
                                , right_schema_id]
                        )
                        first_find = False
                    # print("\t" + right_val)
                    # check if it is formatted as table.column or just table
                    if left_name.count(".") == 1:
                        # column lineage - using DirectionalDataFlow
                        col_writer.writerow(
                            ["core.DirectionalDataFlow", "", "", left_val, right_val]
                        )

                    # write a line to the custom lineage csv file (connection assignment)
                    # col_writer.writerow([leftResource,rightResource,leftRef,rightRef])
                else:
                    missing += 1
                    print("\t no match on right side for key=" + left_name)

        else:
            print("error getting schema info... - no linking/lineage created")

        print(
            module + f":finished. {matches} link(s) created, "
            f"{missing} missing (found in left, no match on right)"
        )
        print("run time = %s seconds ---" % (time.time() - start_time))

        f_csv_file.close()


# call main - if not already called or used by another script
if __name__ == "__main__":
    EDCReplicationLineage(configuration_file="resources/config.json").main()