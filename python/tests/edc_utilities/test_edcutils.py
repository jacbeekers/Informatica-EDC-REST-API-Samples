from edc_rest_api.edc_utilities import edcutils
from edc_rest_api.edc_utilities import encodeUser

# the code in edcutils is provided by Informatica and not properly tested in this project
import csv
import requests
import os

test_url = "http://localhost:8888"
tmp_dir = "/tmp/"


def create_test_file(filename):
    with open(tmp_dir + filename, "w") as file:
        file.write("test")


def remove_test_file(filename):
    try:
        os.remove(tmp_dir + filename)
    except PermissionError or IOError:
        pass


def test_get_fact_value():
    item = { "facts": [{
        "attributeId": "test-attribute",
        "test-property": "ultimate"
    }
    ]}
    value = edcutils.get_fact_value(item, "test-attribute", "test-property")
    assert value == "ultimate"

    value = edcutils.get_fact_value(item, "test-attribute", "doesnotexist-property")
    assert value == ""


def test_exportLineageLink():
    with open("/tmp/testfile.csv", "w", newline='') as file:
        edcutils.exportLineageLink("fromObject", "toObject", "linkType", csv.writer(file))
    pass


def test_getResourceDefUsingSession():
    try:
        edcutils.getResourceDefUsingSession(test_url
                                            , session=requests.session()
                                            , resourceName="dummy-resource"
                                            , sensitiveOptions=True)
    except IOError:
        pass
    pass


def test_createResourceUsingSession():
    try:
        edcutils.createResourceUsingSession(test_url
                                            , session=requests.session()
                                            , resourceName="dummy-resource"
                                            , resourceJson={})
    except IOError:
        pass
    pass


def test_upload_resource_file_using_session():
    filename = "test-resource.zip"
    create_test_file(filename)

    try:
        edcutils.uploadResourceFileUsingSession(test_url
                                                ,session=requests.session()
                                                ,resourceName="test-resource"
                                                ,fileName=filename
                                                ,fullPath=tmp_dir + filename
                                                ,scannerId="FileScanner")
    except IOError:
        pass
    remove_test_file(filename)

    filename = "test-resource.dsx"
    create_test_file(filename)
    try:
        edcutils.uploadResourceFileUsingSession(test_url
                                                ,session=requests.session()
                                                ,resourceName="test-resource"
                                                ,fileName=filename
                                                ,fullPath=tmp_dir + filename
                                                ,scannerId="FileScanner")
    except IOError:
        pass
    remove_test_file(filename)

    pass


def test_execute_resource_load_using_session():

    try:
        edcutils.executeResourceLoadUsingSession(test_url
                                                 ,session=requests.session()
                                                 ,resourceName="test-resource")
    except IOError:
        pass

    pass


def test_encode_user():

    encodeUser.encode(security_domain="", user_name="test", password="test")


def test_create_update_execute_resource_using_session():
    try:
        edcutils.createOrUpdateAndExecuteResourceUsingSession(test_url
                                                              ,session=requests.session()
                                                              ,resourceName="test-resource"
                                                              ,templateFileName="/tmp"
                                                              ,fileName="dummy"
                                                              ,inputFileFullPath="tests/__init__.py"
                                                              ,waitForComplete=True
                                                              ,scannerId="1-1"
                                                              )
    except IOError:
        pass

