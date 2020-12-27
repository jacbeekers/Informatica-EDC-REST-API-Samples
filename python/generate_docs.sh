source venv/bin/activate
pip3 install pdoc3 pydeps >/dev/null
##
# metadata_utilities
##
PACKAGE_NAME=metadata_utilities
#
pdoc3 --force --output-dir docs/$PACKAGE_NAME/markdown src/$PACKAGE_NAME
pdoc3 --force --html --output-dir docs/$PACKAGE_NAME/html src/$PACKAGE_NAME
#
# generate dependency graph
pydeps --log ERROR -o docs/$PACKAGE_NAME/${PACKAGE_NAME}.svg src/$PACKAGE_NAME

##
# edc_utilities
##
PACKAGE_NAME=edc_utilities
pdoc3 --force --output-dir docs/$PACKAGE_NAME/markdown src/$PACKAGE_NAME
pdoc3 --force --html --output-dir docs/$PACKAGE_NAME/html src/$PACKAGE_NAME
#
# generate dependency graph
pydeps --log ERROR -o docs/$PACKAGE_NAME/${PACKAGE_NAME}.svg src/$PACKAGE_NAME
# generate dependency graph for everything in edc_rest_api
pydeps --log ERROR -o docs/overall.svg src

