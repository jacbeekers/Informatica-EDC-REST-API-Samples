source venv/bin/activate
pip3 install pdoc3 pydeps >/dev/null
##
# metadata_utilities
##
PACKAGE_NAME=metadata_utilities
#
pdoc3 --force --output-dir $PACKAGE_NAME/docs/markdown $PACKAGE_NAME
pdoc3 --force --html --output-dir $PACKAGE_NAME/docs/html $PACKAGE_NAME
#
# generate dependency graph
pydeps --log ERROR -o $PACKAGE_NAME/${PACKAGE_NAME}.svg $PACKAGE_NAME

##
# edc_utilities
##
PACKAGE_NAME=edc_utilities
pdoc3 --force --output-dir $PACKAGE_NAME/docs/markdown $PACKAGE_NAME
pdoc3 --force --html --output-dir $PACKAGE_NAME/docs/html $PACKAGE_NAME
#
# generate dependency graph
pydeps --log ERROR -o $PACKAGE_NAME/${PACKAGE_NAME}.svg $PACKAGE_NAME

