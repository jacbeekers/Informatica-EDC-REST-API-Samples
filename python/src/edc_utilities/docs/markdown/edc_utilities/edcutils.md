Module edc_utilities.edcutils
=============================
Created on Aug 2, 2018

utility functions for processing catalog objects

@author: dwrigley

Functions
---------

    
`callGETRestEndpoint(apiURL, user, pWd)`
:   this function call the URL  with a GET method and return the status code
    as well as the response body
    returns rc=200 (valid) & other rc's from the get
            resourceDef (json)

    
`createAttribute(url, user, pWd, attrJson)`
:   create a new attribute
    attrJSON must be in the form
        {
          "items": [
            {
              "analyzer": "INT",
              "boost": "LOWEST",
              "classes": [
                {
                  "id": "string"
                }
              ],
              "dataTypeId": "string",
              "description": "string",
              "facetable": false,
              "multivalued": false,
              "name": "string",
              "searchable": false,
              "sortable": false,
              "suggestable": false
            }
          ]
        }

    
`createOrUpdateAndExecuteResource(url, user, pwd, resourceName, templateFileName, fileName, inputFileFullPath, waitForComplete, scannerId)`
:   create or update resource_name   (note: old way - consider moving to sessions (better for id/pwd/ssl validation))
    upload a file
    execute the scan
    optionally wait for the scan to complete
    
    assumption - from the template, we are only changing the resource name,
                 and filename options - all else is already in the template
    
    @todo:  add a diff process to determine if the input file is different to last time
            - assume last file ins in what folder???

    
`createOrUpdateAndExecuteResourceUsingSession(url, session, resourceName, templateFileName, fileName, inputFileFullPath, waitForComplete, scannerId)`
:   create or update resource_name  (new way with sessions)
    upload a file
    execute the scan
    optionally wait for the scan to complete
    
    assumption - from the template, we are only changing the resource name,
                 and filename options - all else is already in the template
    
    @todo:  add a diff process to determine if the input file is different to last time
            - assume last file ins in what folder???

    
`createResource(url, user, pWd, resourceName, resourceJson)`
:   create a new resource based on the provided JSON
    
    returns rc=200 (valid) & other rc's from the put
            resourceDef (json)

    
`createResourceUsingSession(url, session, resourceName, resourceJson)`
:   create a new resource based on the provided JSON
    using a session that already has the auth (credentials)
    
    returns rc=200 (valid) & other rc's from the put
            resourceDef (json)

    
`executeResourceLoad(url, user, pWd, resourceName)`
:   start a resource load
    
    returns rc=200 (valid) & other rc's from the get
            json with the job details

    
`executeResourceLoadUsingSession(url, session, resourceName)`
:   start a resource load
    
    returns rc=200 (valid) & other rc's from the get
            json with the job details

    
`exportLineageLink(fromObject, toObject, linkType, csvFile)`
:   write a custom lineage line to the csv file
    assumptions
      - csvFile is already created
      - csv header is Association,From Connection,To Connection,From Object,To Object
    Association=linkType, From Object=fromObject,To Object=toObject
    From Connection and To Connection will be empty

    
`getAllResource(url, user, pWd)`
:   get the resource definition - given a resource name (and catalog url)
    catalog url should stop at port (e.g. not have ldmadmin, ldmcatalog etc...
    or have v2 anywhere
    since we are using v1 api's
    
    returns rc=200 (valid) & other rc's from the get
            resourceDef (json)

    
`getCatalogCustomAttr(url, user, pWd)`
:   call GET /access/2/catalog/models/attributes
    this returns all attributes (system + custom)
    filter for only the custom attributes (id startswith "com.infa.appmodels.ldm."

    
`getCatalogObjectCount(url, user, pWd)`
:   get the resource object count - given a catalog url

    
`getCatalogResourceCount(url, user, pWd)`
:   get the resource count - given a catalog url

    
`getResourceDef(url, user, pWd, resourceName, sensitiveOptions=False)`
:   get the resource definition - given a resource name (and catalog url)
    catalog url should stop at port (e.g. not have ldmadmin, ldmcatalog etc...
    or have v2 anywhere
    since we are using v1 api's
    
    returns rc=200 (valid) & other rc's from the get
            resourceDef (json)

    
`getResourceDefUsingSession(url, session, resourceName, sensitiveOptions=False)`
:   get the resource definition - given a resource name (and catalog url)
    catalog url should stop at port (e.g. not have ldmadmin, ldmcatalog etc...
    or have v2 anywhere
    since we are using v1 api's
    
    returns rc=200 (valid) & other rc's from the get
            resourceDef (json)

    
`getResourceObjectCount(url, user, pWd, resourceName)`
:   get the resource object count - given a resource name (and catalog url)

    
`getReusableScannerConfig(url, user, pWd)`
:   get the reusable configuration - given a catalog url

    
`get_fact_value(item, attribute_name, json_property)`
:   returns the value of a fact (attribute) from an item
    
    iterates over the "facts" list - looking for a matching attributeId
    to the parameter attribute_name
    returns the "value" json_property or ""

    
`updateResourceDef(url, user, pWd, resourceName, resJson)`
:   update a setting in an existing resource
    
    returns rc=200 (valid) & other rc's from the put
            resourceDef (json)

    
`uploadResourceFile(url, user, pWd, resourceName, fileName, fullPath, scannerId)`
:   upload a file for the resource - e.g. a custom lineage csv file
    works with either csv for zip files  (.csv|.zip)
    
    returns rc=200 (valid) & other rc's from the post

    
`uploadResourceFileUsingSession(url, session, resourceName, fileName, fullPath, scannerId)`
:   upload a file for the resource - e.g. a custom lineage csv file
    works with either csv for zip files  (.csv|.zip)
    
    returns rc=200 (valid) & other rc's from the post