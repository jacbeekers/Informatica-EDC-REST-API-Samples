"""
Created on Aug 10, 2018

Note:  this is the python 3.x version

base64 encode - prompting for security domain, username and password
this is useful for generating the string used for API basic authentication

the user will be prompted for an id and password and optional security domain
& print the encoded result to the console

@author: dwrigley
"""

import base64
import getpass


def encode(security_domain=None, user_name=None, password=None):
    if security_domain is None:
        print("")
        print("Enter values for Security Domain (optional), User and Password")
        secDomain = input("security domain <empty> for Native:")
    else:
        secDomain = security_domain
    if user_name is None:
        u = input("User Name for catalog:")
    else:
        u = user_name
    if password is None:
        p = getpass.getpass(prompt="password for user=" + u + ":")
    else:
        p = password
    if secDomain == "":
        auth_str = f"{u}:{p}"
    else:
        auth_str = f"{secDomain}\\{u}:{p}"
    b64_auth_str = base64.b64encode(bytes(auth_str, "utf-8"))

    # print result of encoding to console
    # print(b64_auth_str.decode("utf-8"))
    print("header settings:")
    print(f'\t"Authorization": Basic {b64_auth_str.decode("utf-8")}')

    print("\nto set an env variable - linux/mac:")
    print(f'\texport INFA_EDC_AUTH="Basic {b64_auth_str.decode("utf-8")}"')
    print("")
    print("for Powershell:")
    print(f'\t$env:INFA_EDC_AUTH="Basic {b64_auth_str.decode("utf-8")}"')
    print("")
    print("for windows cmd:")
    print(f'\tset INFA_EDC_AUTH=Basic {b64_auth_str.decode("utf-8")}')
    print("")

    print("finished")
    return b64_auth_str.decode("utf-8")


if __name__ == '__main__':
    encode()
