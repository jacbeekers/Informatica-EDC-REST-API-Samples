"""
defines a class to help with edc connections & uses requests.session to store
credentials & verify settings for each subsequent api call

will use these env variables, if they exist (default)
    INFA_EDC_URL
    INFA_EDC_AUTH
    INFA_EDC_SSL_PEM

uses command-line args to easily define common connection properties for edc
    these properties will over-ride what is stored in env-vars
    -c --edcurl  http(s)://catalogserver:port
    -a --auth    base64 encoded credentials see encodeUser.py
    -u --user    (not preferred) but can be passed (will prompt for pwd)
    -s --sslcert https certificate if needed

Usage:
    edcSession = EDCSession()
    edcSession.init_edc_session()

    ...
    resp = edcSession.session.get(resourceUrl, params=(), edc_timeout=10)

Note: this is syncronyous version - not async
"""
import argparse
import os
import warnings
from urllib.parse import urljoin

import requests

from src.metadata_utilities import messages

warnings.filterwarnings('ignore', message='Unverified HTTPS request')


class EDCSession:
    """
    encapsulates argparse based command-line parser & requests.session object
    for easy re-use for multiple scripts
    """

    def __init__(self, settings):
        self.baseUrl = settings.edc_url
        self.session: requests.session = None
        self.argparser = argparse.ArgumentParser(add_help=False)
        self.__setup_standard_cmdargs__()
        self.edcversion = 0
        self.http_proxy = None
        self.https_proxy = None
        self.settings = settings
        self.timeout = settings.edc_timeout
        self.mu_log = self.settings.mu_log
        self.session = self.init_edc_session()

    def __setup_standard_cmdargs__(self):
        # check for args overriding the env vars
        self.argparser.add_argument(
            "-c",
            "--edcurl",
            required=False,
            help=(
                "edc url  - including http(s)://<server>:<port>, "
                "if not already configured via INFA_EDC_URL environment var "
            ),
            type=str,
        )
        group = self.argparser.add_mutually_exclusive_group()
        group.add_argument(
            "-a",
            "--auth",
            required=False,
            help=(
                "basic authorization encoded string (preferred over -u) "
                "if not already configured via INFA_EDC_AUTH environment var"
            ),
            type=str,
        )
        group.add_argument(
            "-u",
            "--user",
            required=False,
            help="user name",
            type=str,
        )
        self.argparser.add_argument(
            "-x",
            "--http_proxy",
            required=False,
            help="HTTP Proxy",
            type=str,
        )
        self.argparser.add_argument(
            "-X",
            "--https_proxy",
            required=False,
            help="HTTPS Proxy",
            type=str,
        )
        self.argparser.add_argument(
            "-s",
            "--sslcert",
            required=False,
            help=(
                "ssl certificate (pem format), if not already configured "
                "via INFA_EDC_SSL_PEM environment var"
            ),
            type=str,
        )

    def init_edc_session(self):
        """
        reads the env vars and any command-line parameters & creates an edc session
        with auth and optionally verify attributes populated (shared so no need to use
        on individual calls)
        returns:
            url, auth
        """
        module = __name__ + ".init_edc_session"
        auth = None
        verify = None

        args, unknown = self.argparser.parse_known_args()
        if "INFA_EDC_URL" in os.environ:
            self.baseUrl = os.environ["INFA_EDC_URL"]
            print("\t\tusing EDC_URL=" + self.baseUrl + " from INFA_EDC_URL environment variable")

        auth = self.settings.edc_auth
        if args.auth is not None:
            print(f"\t\tusing edc auth from command-line parameter.")
            auth = args.auth
        else:
            if "INFA_EDC_AUTH" in os.environ:
                print("\t\tusing INFA_EDC_AUTH from environment")
                auth = os.environ["INFA_EDC_AUTH"]
                # print(f"value = {auth}")

        if "INFA_EDC_SSL_PEM" in os.environ:
            verify = os.environ["INFA_EDC_SSL_PEM"]
            print("\t\tusing ssl certificate from env var INFA_EDC_SSL_PEM=" + verify)

        if "HTTP_PROXY" in os.environ:
            self.http_proxy = os.environ["HTTP_PROXY"]
            print("\t\tusing HTTP Proxy from env var HTTP_PROXY=" + self.http_proxy)

        if "HTTPS_PROXY" in os.environ:
            self.https_proxy = os.environ["HTTPS_PROXY"]
            print("\t\tusing HTTPS Proxy from env var HTTPS_PROXY=" + self.https_proxy)

        # check the catalog url & user command-line
        if args.edcurl is not None:
            if self.baseUrl != args.edcurl:
                print(f"\t\tusing edc url from command-line parameter {args.edcurl}")
                self.baseUrl = args.edcurl
        # if there is still no edc url - then use it from edc secrets file
        if self.baseUrl is None:
            print(f"\t\tusing edc url from edc secrets file")
            self.baseUrl = self.settings.edc_url

        if args.sslcert is not None:
            if args.sslcert == "False":
                verify = False
            else:
                verify = args.sslcert

        # create a session
        self.session = requests.Session()
        self.session.verify = verify
        self.session.headers.update({"Accept": "application/json"})
        # self.session.headers.update({"Content-Type": "application/json; charset=utf8"})
        self.session.headers.update({"Content-Type": "application/json"})
        self.session.headers.update({"Authorization": auth})
        self.mu_log.log(self.mu_log.DEBUG, "Authorization header was set.", module)
        self.session.baseUrl = self.baseUrl
        self.validate_edc_connection()
        return self.session

    def configure_edc_session(self, catalog_url, catalog_auth, verify):
        """
        given a valid URL and auth - setup a requests session to use
        for subsequent calls, verify can be False
        """
        self.session = requests.Session()
        self.baseUrl = catalog_url
        self.session.baseUrl = self.baseUrl
        self.session.headers.update({"Authorization": catalog_auth})
        if verify is None:
            verify = False
        self.session.verify = verify
        return messages.message["ok"]

    def validate_edc_connection(self):
        module = __name__ + ".validate_edc_connection"
        """
        validate that the connection informatioon (url + auth credentials)
        are correct.
        returns:
            status code (e.g. 200 for ok)
            json message ()
        """
        self.mu_log.log(self.mu_log.DEBUG, "validating connection to: " + self.session.baseUrl, module)
        try:
            url = urljoin(self.baseUrl, "access/2/catalog/data/productInformation")
            proxies = {"http": self.http_proxy
                , "https": self.https_proxy}
            # url = self.baseUrl + "access/2/catalog/data/productInformation"
            resp = self.session.get(url, timeout=self.timeout, proxies=proxies)
            self.mu_log.log(self.mu_log.DEBUG, "api status code=>" + str(resp.status_code) + "<.", module)
            if resp.status_code == 200:
                # valid and 10.4+, get the actual version
                rel_version = resp.json().get("releaseVersion")
                if rel_version.count(".") == 2:
                    # version is something like 10.4.0
                    # but we need to make it a 4 part name like 10.4.0.0
                    rel_version = rel_version + ".0"
                # remove the "." from the version
                rel_nbr = rel_version.replace(".", "")
                self.edcversion = rel_nbr
                self.mu_log.log(self.mu_log.INFO, "EDC Release version=" + rel_version, module)
                self.mu_log.log(self.mu_log.DEBUG, "Response headers: " + str(resp.headers), module)
                return resp.status_code, resp.json()
            elif resp.status_code == 400:
                self.mu_log.log(self.mu_log.WARNING, "catalog server is not v10.4 or later - trying another method..."
                                , module)
                # invalid request - try another api call
                url = urljoin(self.baseUrl, "access/1/catalog/data")
                resp = self.session.get(url, timeout=self.timeout)
                self.mu_log.log(self.mu_log.DEBUG, "2nd try status code: " + str(resp.status_code), module)
            else:
                self.mu_log.log(self.mu_log.ERROR, "error connecting: " + str(resp.json()), module)
            return resp.status_code, resp.json()
        except requests.exceptions.RequestException as e:
            self.mu_log.log(self.mu_log.ERROR, "Error connecting to : " + self.session.baseUrl, module)
            # exit if we can't connect
            return 0, None
