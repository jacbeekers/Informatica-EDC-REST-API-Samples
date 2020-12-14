How to use metadata_utilities
=============================

## To be extended soon

## Prerequisites

For more on the configuration files, check the [configuration docs](https://github.com/jacbeekers/Informatica-EDC-REST-API-Samples/tree/master/python/resources/schemas/config)

* resources/config.json
* resources/edc_config.json
* resources/log_config.json
* resources/azure_monitor.secrets - only needed if you want to use opencensus
* resources/edc_connectivity.secrets (not needed when using .env)
* dependencies listed in requirements.txt (opencensus only needed if you want to use it)

Check the *.secrets.example files for, well, examples.

## Prepare running the code

* Setup your virtual environment and install informatica-edc-rest-api-samples. You may want to get it from test.pypi.org if you want a preview and test that.
```shell script
   mkdir log
   mkdir out
   python3 -m venv venv
   source venv/bin/activate
   # on Windows: venv\Scripts\activate
   # upgrade pip to avoid constant warnings
   python3 -m pip install --upgrade pip
   pip3 install informatica-edc-rest-api-samples
```
* Note: The code above assumes you've already configured your pip through a pip.conf or pip.ini

* Create a small python code, e.g. run_edc_lineage.py similar to the example:
```python
from src.metadata_utilities import load_json_metadata


def main():
    # Change the path+file to the main configuration file you want the code to use
    result = load_json_metadata.ConvertJSONtoEDCLineage("/tmp/resources/config.json").main()
    if result["code"] == "OK":
       exit(0)
    else:
       exit(1)
          

if __name__ == "__main__":
   main()

```


## Running the code
Activate the above created venv in which you installed informatica-edc-rest-api-samples:
```shell script
   source venv/bin/activate
   python3 run_edc_lineage.py
```


### Run it from PyCharm

[Screenshot of the PyCharm runconfig used for unit tests](docs/RunConfig-PyCharm.png)
