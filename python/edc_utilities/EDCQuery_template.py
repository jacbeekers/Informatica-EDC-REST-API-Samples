"""
Created on Jul 16, 2018

@author: dwrigley

This template can be copied & used to query the catalog
and process each item returned individually (in processAnItem)
it handles the paging model (see pageSize variable)

"""

import time

from edc_utilities import edcutils, edcSessionHelper

# set edc helper session + variables (easy/re-usable connection to edc api)
edcHelper = edcSessionHelper.EDCSession()

def process_item(an_item, item_count):
    """
    put your code here - that does something with the item
    for this example, just print the it and name
    @note python 2.7 does not allow us to specify the parameter type...
    """
    item_id = an_item["id"]
    item_name = edcutils.get_fact_value(an_item, "core.name", "value")
    provider_id = edcutils.get_fact_value(an_item, "core.name", "providerId")
    xid = edcutils.get_fact_value(an_item, "core.name", "xid")
    print("\titemId=" + item_id)
    print("\t\titemName=" + item_name)
    print("\t\tproviderId=" + provider_id)
    print("\t\txid=" + xid)


def main():
    """
    main starts here - run the query processing all items
    note:  this version supports the paging model, to process the results
           in chunks of pageSize
    """
    start_time = time.time()
    total = 1000  # initial value - set to > 0 - will replaced on first call
    offset = 0
    page = 0

    edcHelper.initUrlAndSessionFromEDCSettings()
    print("EDC_query_template:start")
    print(f"Catalog={edcHelper.baseUrl}")

    url = edcHelper.baseUrl + "/access/2/catalog/data/objects"
    print(f"url={url}")

    edc_resource_name = "demoSource"

    query = " core.allclassTypes:( \
            com.infa.ldm.relational.Table  \
            com.infa.ldm.relational.Column  \
            com.infa.ldm.relational.ViewColumn  \
            com.infa.ldm.file.delimited.DelimitedField  \
            com.infa.ldm.file.xml.XMLFileField  \
            com.infa.ldm.file.json.JSONField  \
            com.infa.ldm.adapter.Field  \
            com.infa.ldm.file.avro.AVROField  \
            com.infa.ldm.file.parquet.PARQUETField \
            core.Dataset \
            ) \
            and core.resourceName:" + edc_resource_name

    print("\tquery=" + query)

    schema_id = None
    table_count = 0
    column_count = 0
    global itemCount
    itemCount = 0

    pageSize = 10000  # e.g. 10 objects for each page/chunk - change as needed

    while offset < total:
        page_time = time.time()
        parameters = {'q': query, 'offset': offset, 'pageSize': pageSize}
        page += 1
        response = edcHelper.session.get(url, params=parameters, timeout=3)
        print(f"session finished with: {response.status_code}")
        #        response_old = requests.get(url, params=parameters, headers=header,
        #                            auth=HTTPBasicAuth(uid, pwd))
        status = response.status_code
        if status != 200:
            # some error - e.g. catalog not running, or bad credentials
            print("error! " + str(status) + str(response.json()))
            break

        result_json = response.json()
        print(result_json)
        total = result_json['metadata']['totalCount']
        print(f"objects found: {total} offset: {offset} "
              f"pagesize={pageSize} currentPage={page} "
              f"objects {offset + 1} - {offset + pageSize}"
              )

        # for next iteration
        offset += pageSize

        for foundItem in result_json["items"]:
            itemCount += 1
            process_item(an_item=foundItem, item_count=itemCount)

        # end of page processing
        print("\tpage processed - %s seconds ---" % (time.time() - page_time))

    # end of while loop
    print("Finished - run time = %s seconds ---" % (time.time() - start_time))


# call main - if not already called or used by another script
if __name__ == "__main__":
    main()
