How to use metadata_utilities
=============================

## To be extended soon

## Prerequisites

* .env - check the original github project for more info on this file. Also check the .env.example file
* resources/config.json
* resources/edc_config.json
* resources/azure_monitor.secrets - only needed if you want to use opencensus
* resources/edc_connectivity.secrets (not needed when using .env)
* dependencies listed in requirements.txt (opencensus only needed if you want to use it)

Check the *.secrets.example files for, well, examples.

## Running the code

The main python script is [load_json_metadata.py](load_json_metadata.py)

### Run it from PyCharm

[Screenshot of the PyCharm runconfig used for unit tests](docs/RunConfig-PyCharm.png)
