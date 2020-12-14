#
# Script to install from test.pypi and run the code
#
clear
mkdir -p log
mkdir -p out
mkdir <your_directory_to_store_json_input_files>
# copy the json files in the directory. You need to change the config.json accordingly
mkdir <your_directory_to_store_configuration_files>
# copy the example configuration files from https://github.com/jacbeekers/Informatica-EDC-REST-API-Samples/tree/master/python/resources
#  and modify them to your needs
mkdir <your_directory_that_stores_the_metadata_interface_schemas>
# copy the interface schemas from https://github.com/jacbeekers/metadata-registry-interface-specifications/tree/master/metadata/schemas/interface
# December 2020 version is 0.2.0
#
# Remove the old virtual environment, if any
rm -rf venv/
# create a new virtual environment
python3 -m venv venv
# activate it
source venv/bin/activate
# install the package
# - test.pypi.org always contains the latest version
# - pypi.org only contains tested versions
# You may need to add your proxy and trusted hosts
pip install --extra-index-url https://test.pypi.org/simple/ informatica-edc-rest-api-samples
#
# Run create custom attributes to create the expected EDC Custom Attributes
python3 add_custom_attributes.py
#
# Load lineage information based on the JSON directory configured in config.json
python3 run_edc_lineage.py

#
# More info on configuration: https://github.com/jacbeekers/Informatica-EDC-REST-API-Samples/blob/master/python/docs/EDC%20REST%20API%20configuration%20files.png
#