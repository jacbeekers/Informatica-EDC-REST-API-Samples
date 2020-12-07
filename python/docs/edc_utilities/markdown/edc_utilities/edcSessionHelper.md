Module edc_utilities.edcSessionHelper
=====================================
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
    edcSession.initUrlAndSessionFromEDCSettings()

    ...
    resp = edcSession.session.get(resourceUrl, params=(), timeout=10)

Note: this is syncronyous version - not async

Classes
-------

`EDCSession(settings)`
:   encapsulates argparse based command-line parser & requests.session object
    for easy re-use for multiple scripts

    ### Methods

    `initSession(self, catalog_url, catalog_auth, verify)`
    :   given a valid URL and auth - setup a requests session to use
        for subsequent calls, verify can be False

    `initUrlAndSessionFromEDCSettings(self, edc_secrets='resources/edc.secrets')`
    :   reads the env vars and any command-line parameters & creates an edc session
        with auth and optionally verify attributes populated (shared so no need to use
        on individual calls)
        returns:
            url, auth

    `validateConnection(self)`
    :   validate that the connection informatioon (url + auth credentials)
        are correct.
        returns:
            status code (e.g. 200 for ok)
            json message ()