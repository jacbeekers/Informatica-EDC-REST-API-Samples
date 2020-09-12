Module edc_utilities.EDCQuery_template
======================================
Created on Jul 16, 2018

@author: dwrigley

This template can be copied & used to query the catalog
and process each item returned individually (in processAnItem)
it handles the paging model (see pageSize variable)

Functions
---------

    
`main()`
:   main starts here - run the query processing all items
    note:  this version supports the paging model, to process the results
           in chunks of pageSize

    
`process_item(an_item, item_count)`
:   put your code here - that does something with the item
    for this example, just print the it and name
    @note python 2.7 does not allow us to specify the parameter type...