import re

import setuptools

# https://packaging.python.org/tutorials/packaging-projects/

with open("README.md", "r") as fh:
    long_description = fh.read()

version_file = 'resources/version.py'
tmp_version_file = 'temp/_tmp_version.tmp'

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open(version_file, 'rb') as f:
    for line in f:
        line = line.strip()
        if line:
            line = line.decode('utf-8')
            reg_comment = re.compile(r'^#.*')
            m = reg_comment.search(line)
            if not m:
                result_search = _version_re.search(line)
                version = result_search.group(1)
                version = version.strip('\"')
                main_version, sub_version, fix_version = version.split(".")
                fix_number = int(fix_version) + 1
                new_version = main_version + "." + sub_version + "." + str(fix_number)

                with open(tmp_version_file, 'wb') as t:
                    out_line = '__version__ = "' + new_version + '"\n'
                    t.write(out_line.encode('utf-8'))

setuptools.setup(
    name='informatica-edc-rest-api-samples',
    version=new_version,
    author='Jac. Beekers',
    author_email='beekersjac@gmail.com',
    description="Examples how to use the Informatica EDC samples. Loosely based on Informatica's EDC-REST-API-Samples",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/jacbeekers/Informatica-EDC-REST-API-Samples',
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
        'urllib3',
        'jinja2',
        'opencensus-ext-azure',
        'opencensus-ext-requests',
        'jsonschema'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.6'
)
