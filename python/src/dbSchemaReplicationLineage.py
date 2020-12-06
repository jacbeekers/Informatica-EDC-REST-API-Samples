"""
Created on Jun 26, 2018

@author: dwrigley
***************************************************************************************
DB schema replication custom lineage generator

process:-
    scenario:  the tables in 2 different schemas
    (perhaps in different databases/resources) are replicated
    in EDC - we have no way to automatically know that there is lineage
    between the schema contents (tables & columns)
    this utility will generate the custom lineage import to create the links

    given two schemas - leftSchema and rightSchema
    find the 2 schemas objects in the catalog (GET /2/catalog/data/objects)

    for each schema
        execute /2/catalog/data/relationships (2 levels schema->table->column)
            for each table & column - store the id & name (names converted to
            lower-case for case-insensitive match)

    for the stored objects (tables/columns) left side...
        find the same table/column in the right side
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
import time

from src.edc_utilities import edcSessionHelper, edcutils

# set edc helper session + variables (easy/re-usable connection to edc api)
edcHelper = edcSessionHelper.EDCSession()

# define script command-line parameters (in global scope for gooey/wooey)
parser = argparse.ArgumentParser(parents=[edcHelper.argparser])
# add args specific to this utility (left/right resource, schema, classtype...)
parser.add_argument(
    "-lr", "--leftresource", required=True, help="name of the left resource to find objects"
)
parser.add_argument(
    "-ls", "--leftschema", required=True, help="name of the left schema/container object"
)
parser.add_argument(
    "-lt", "--lefttype", required=False, default="com.infa.ldm.relational.Schema",
    help="class type for the schema level object"
)
parser.add_argument(
    "-rr", "--rightresource", required=True, help="name of the right resource to find objects"
)
parser.add_argument(
    "-rs", "--rightschema", required=True, help="name of the right schema/container object"
)
parser.add_argument(
    "-rt", "--righttype", required=False, default="com.infa.ldm.relational.Schema",
    help="class type for the right schema level object"
)
parser.add_argument(
    "-pfx", "--csvprefix", required=False, default="schemaLineage",
    help="prefix to use when creating the output csv file"
)
parser.add_argument(
    "-rtp", "--righttableprefix", required=False, default="", help="table prefix for right datasets"
)
parser.add_argument(
    "-o",
    "--outDir",
    default="out",
    required=False,
    help=(
        "output folder to write results - default = ./out "
        " - will create folder if it does not exist"
    ),
)


def get_schema_objects(schema_name, schema_type, resource_name):
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
    print("\tget_schema_objects for:" + schema_name + " resource=" + resource_name)
    # schemaDict returned  key=TABLE.COLUMN value=column id
    schema_dict = {}
    table_names = {}

    # url = catalogServer + "/access/2/catalog/data/objects"
    url = edcHelper.baseUrl + "/access/2/catalog/data/objects"
    query = (f'+core.resourceName:"{resource_name}"'
             + f' +core.classType:"{schema_type}"'
             + f' +core.name:"{schema_name}"'
             )
    parameters = {"q": query, "offset": 0, "pageSize": 1}
    print("\tquery=" + query)

    schema_id = None
    table_count = 0
    column_count = 0
    # make the call to find the schema object
    response = edcHelper.session.get(url, params=parameters, timeout=3)
    print(f"session get finished: {response.status_code}")
    rc = response.status_code

    if rc != 200:
        print("error reading object: rc=" + str(rc) + " response:" + str(response.json))
        if rc == 401:
            print(
                "\t401:Possible Missing/bad credentials"
            )
            print(str(response))
        return

    # get the total # of objects returned (first part of the json resultset)
    total_objects = response.json()["metadata"]["totalCount"]
    print("\tobjects returned: " + str(total_objects))

    for item in response.json()["items"]:
        schema_id = item["id"]
        schema_name = edcutils.get_fact_value(item, "core.name")
        # get the tables & columns
        print("\tfound schema: " + schema_name + " id=" + schema_id)

        lineage_url = edcHelper.baseUrl + "/access/2/catalog/data/relationships"
        lineage_parms = {
            "seed": schema_id,
            "association": "core.ParentChild",
            "depth": "2",
            "direction": "OUT",
            "includeAttribute": {"core.name", "core.classType"},
            "includeTerms": "false",
            "removeDuplicateAggregateLinks": "false",
        }
        print(
            "\tGET child rels for schema: " + lineage_url + " parms=" + str(lineage_parms)
        )
        # get using uid/pwd
        lineage_response = edcHelper.session.get(
            lineage_url,
            params=lineage_parms,
        )
        lineage_status = lineage_response.status_code
        print("\tlineage resp=" + str(lineage_status))
        if lineage_status != 200:
            print(
                f"error getting schema contents (tables) rc={rc}"
                f" response:{response.json}"
            )
            if rc == 401:
                print(
                    "\t401:Possible Missing/bad credentials"
                )
                print(str(response))
            return

        if lineage_response.text.startswith("{items:"):
            # bug (10.2.0 & 10.2.1) - the items collection should be "items"
            lineage_json = lineage_response.text.replace("items", '"items"', 1)
        else:
            lineage_json = lineage_response.text
        # relsJson = json.loads(lineageJson.replace('items', '"items"'))
        rels_json = json.loads(lineage_json)
        # print(len(relsJson))

        for lineageItem in rels_json["items"]:
            # print('\t\t' + str(lineageItem))
            in_id = lineageItem.get("inId")
            out_id = lineageItem.get("outId")

            # print('new inId===' + inId + " outId=" + outId)
            # print(edcutils.get_fact_value(lineageItem["inEmbedded"], "core.name"))
            assoc_id = lineageItem.get("associationId")
            # print("\t\t" + inId + " assoc=" + assocId)
            # if assocId=='com.infa.ldm.relational.SchemaTable':
            if assoc_id.endswith(".SchemaTable"):
                # note - custom lineage does not need table and column
                # count the tables & store table names
                table_count += 1
                # tableName = inId.split('/')[-1]
                table_name = edcutils.get_fact_value(
                    lineageItem["inEmbedded"], "core.name"
                ).lower()
                # store the table name (for lookup when processing the columns)
                # key=id, val=name
                table_names[in_id] = table_name
                schema_dict[table_name] = in_id
            # if assocId=='com.infa.ldm.relational.TableColumn':
            if assoc_id.endswith(".TableColumn") or assoc_id.endswith(
                    ".TablePrimaryKeyColumn"
            ):
                # columnName = inId.split('/')[-1]
                column_count += 1
                column_name = edcutils.get_fact_value(
                    lineageItem["inEmbedded"], "core.name"
                ).lower()
                table_name = table_names[out_id].lower()
                # print("column=" + tableName + "." + columnName)
                schema_dict[table_name + "." + column_name] = in_id

    print(
        "\tgetSchema: returning "
        + str(column_count)
        + " columns, in "
        + str(table_count)
        + " tables"
    )
    return schema_dict, schema_id


def main():
    """
    initialise the csv file(s) to write
    call get_schema_objects for both left and right schema objects
    match the tables/columns from the left schema to the right
    when matched
        write a lineage link - table and column level

    Note:  this script generates the newer lineage format using complete
           object id's and relationship types
           connection assignment will not be necessary
           works with v10.2.1+

    """
    args = args, unknown = parser.parse_known_args()
    # setup edc session and catalog url - with auth in the session header,
    # by using system vars or command-line args
    edcHelper.initUrlAndSessionFromEDCSettings()

    print(f"command-line args parsed = {args} ")

    start_time = time.time()

    print("dbSchemaReplicationLineage:start")
    print(f"Catalog={edcHelper.baseUrl}")
    print(f"left:  resource={args.leftresource}")
    print(f"left:    schema={args.leftschema}")
    print(f"left:      type={args.lefttype}")
    print(f"right:  resource={args.rightresource}")
    print(f"right:    schema={args.rightschema}")
    print(f"right:      type={args.righttype}")
    print(f"output folder:{args.outDir}")
    print(f"output file prefix:{args.csvprefix}")
    print(f"right table prefix:{args.righttableprefix}")

    # initialize csv output file
    column_header = [
        "Association",
        "From Connection",
        "To Connection",
        "From Object",
        "To Object",
    ]

    # set the csv fileName
    csv_file_name = (
        f"{args.outDir}/{args.csvprefix}_{args.leftschema.lower()}"
        f"_{args.rightschema.lower()}.csv"
    )
    # python 3 & 2.7 use different methods
    print("initializing file: " + csv_file_name)
    f_csv_file = open(csv_file_name, "w", newline="", encoding="utf-8")
    col_writer = csv.writer(f_csv_file)
    col_writer.writerow(column_header)

    # get the objects from the left schema into memory
    print(
        f"get left schema: name={args.leftschema}"
        f" resource={args.leftresource}"
        f" type={args.lefttype}"
    )
    left_objects, left_schema_id = get_schema_objects(
        args.leftschema, args.lefttype, args.leftresource
    )

    # get the objects from the right schema into memory
    print(
        f"get right schema: name={args.rightschema}"
        f" resource={args.rightresource}"
        f" type={args.righttype}"
    )
    right_objects, right_schema_id = get_schema_objects(
        args.rightschema, args.righttype, args.rightresource
    )

    matches = 0
    missing = 0

    if len(left_objects) > 0 and len(right_objects) > 0:
        # create the lineage file
        col_writer.writerow(
            ["core.DataSourceDataFlow", "", "", left_schema_id, right_schema_id]
        )
        # iterate over all left objects - looking for matching right ones
        print("\nprocessing: " + str(len(left_objects)) + " objects (left side)")
        for left_name, leftVal in left_objects.items():
            # if the target is using a prefix - add it to leftName
            if len(args.righttableprefix) > 0:
                left_name = args.righttableprefix.lower() + left_name

            # print("key=" + left_name + " " + leftVal + " " + str(left_name.count('.')))
            if left_name in right_objects.keys():
                # match
                right_val = right_objects.get(left_name)
                matches += 1
                # print("\t" + right_val)
                # check if it is formatted as table.column or just table
                if left_name.count(".") == 1:
                    # column lineage - using DirectionalDataFlow
                    col_writer.writerow(
                        ["core.DirectionalDataFlow", "", "", leftVal, right_val]
                    )
                else:
                    # table level - using core.DataSetDataFlow
                    col_writer.writerow(
                        ["core.DataSetDataFlow", "", "", leftVal, right_val]
                    )

                # write a line to the custom lineage csv file (connection assignment)
                # colWriter.writerow([leftResource,rightResource,leftRef,rightRef])
            else:
                missing += 1
                print("\t no match on right side for key=" + left_name)

    else:
        print("error getting schema info... - no linking/lineage created")

    print(
        f"dbSchemaLineageGen:finished. {matches} links created, {missing} missing (found in left, no match on right)"
    )
    print("run time = %s seconds ---" % (time.time() - start_time))

    f_csv_file.close()


# call main - if not already called or used by another script
if __name__ == "__main__":
    main()
