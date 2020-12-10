Module edc_utilities.edcutils
=============================
Created on Aug 2, 2018

utility functions for processing catalog objects

@author: dwrigley

Functions
---------

    
`createOrUpdateAndExecuteResourceUsingSession(url, session, resourceName, templateFileName, fileName, inputFileFullPath, waitForComplete, scannerId)`
:   create or update resource_name  (new way with sessions)
    upload a file
    execute the scan
    optionally wait for the scan to complete
    
    assumption - from the template, we are only changing the resource name,
                 and filename options - all else is already in the template
    
    @todo:  add a diff process to determine if the input file is different to last time
            - assume last file ins in what folder???

    
`createResourceUsingSession(url, session, resourceName, resourceJson)`
:   create a new resource based on the provided JSON
    using a session that already has the auth (credentials)
    
    returns rc=200 (valid) & other rc's from the put
            resourceDef (json)

    
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

    
`getResourceDefUsingSession(url, session, resourceName, sensitiveOptions=False)`
:   get the resource definition - given a resource name (and catalog url)
    catalog url should stop at port (e.g. not have ldmadmin, ldmcatalog etc...
    or have v2 anywhere
    since we are using v1 api's
    
    returns rc=200 (valid) & other rc's from the get
            resourceDef (json)

    
`get_fact_value(item, attribute_name, json_property)`
:   returns the value of a fact (attribute) from an item
    
    iterates over the "facts" list - looking for a matching attributeId
    to the parameter attribute_name
    returns the "value" json_property or ""

    
`uploadResourceFileUsingSession(url, session, resourceName, fileName, fullPath, scannerId)`
:   upload a file for the resource - e.g. a custom lineage csv file
    works with either csv for zip files  (.csv|.zip)
    
    returns rc=200 (valid) & other rc's from the post