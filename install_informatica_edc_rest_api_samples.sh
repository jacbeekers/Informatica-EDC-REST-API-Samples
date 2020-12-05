#
# Script to install from test.pypi and run the code
#
clear
rm -rf venv/
python3 -m venv venv
source venv/bin/activate
pip install --extra-index-url https://test.pypi.org/simple/ informatica-edc-rest-api-samples
python3 run_edc_lineage.py

