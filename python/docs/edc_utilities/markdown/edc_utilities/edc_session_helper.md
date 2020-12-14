Module edc_utilities.edc_session_helper
=======================================
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

Classes
-------

`EDCSession(settings)`
:   encapsulates argparse based command-line parser & requests.session object
    for easy re-use for multiple scripts

    ### Methods

    `configure_edc_session(self, catalog_url, catalog_auth, verify)`
    :   given a valid URL and auth - setup a requests session to use
        for subsequent calls, verify can be False

    `init_edc_session(self)`
    :   reads the env vars and any command-line parameters & creates an edc session
        with auth and optionally verify attributes populated (shared so no need to use
        on individual calls)
        returns:
            url, auth

    `validate_edc_connection(self)`
    :