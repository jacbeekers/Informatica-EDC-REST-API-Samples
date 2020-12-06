# Informatica EDC REST-API-Samples for Python
This repository contains Python samples for EDC's REST API. 
Forked from Informatica-EIC/REST-API-Samples. Removed Java source.

Official REST API documents can be found [here](https://docs.informatica.com/data-catalog/enterprise-data-catalog/10-4-1/enterprise-data-catalog-rest-api-reference)

Getting Started
---------------

* Create a virtual environment:
  python3 -m venv venv
* Activate the virtual environment:
  source venv/bin/activate
* Install the package
  * The latest version from test.pypi.org:
    pip3 install --extra-index-url https://test.pypi.org/simple/ informatica-edc-rest-api-samples
  * The tested version from pypi.org:
    pip3 install informatica-edc-rest-api-samples
* Run the code
    python3 run_edc_lineage.py

Note: Check the coverage information available in [coverage overview](python/docs/htmlcoverage)

Contributing
------------

* Clone this repository
* This repository uses one submodules. Run the following the get it:
  - git submodule init
  - git submodule update
The git repository metadata-registry-interface-specifications will be located in Informatica-EDC-REST-API-Samples/python/metadata-registry-specifications

## More into on the metadata_utilities
[Dependency Graph](python/metadata_utilities/docs/metadata_utilities.svg)

[Documentation](python/metadata_utilities/docs/markdown/metadata_utilities/index.md)

[Documentation as html](python/metadata_utilities/docs/html/metadata_utilities/index.html)

[Usage](python/metadata_utilities/usage.md)


## More info on the edc_utilities
(these are used by the metadata_utilities)

[Dependency Graph](python/edc_utilities/docs/edc_utilities.svg)

[Documentation](python/edc_utilities/docs/markdown/edc_utilities/index.md)

[Documentation as html](python/edc_utilities/docs/html/edc_utilities/index.html)

[Usage](python/edc_utilities/usage.md)

## Package on PyPI

[We are on PyPI](https://pypi.org/project/informatica-edc-rest-api-samples/)

