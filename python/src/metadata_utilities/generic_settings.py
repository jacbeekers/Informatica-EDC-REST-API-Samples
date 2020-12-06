import json

from src.metadata_utilities import messages
from src.metadata_utilities import mu_logging


class GenericSettings:
    """
    Some generic utilities, e.g. reading the config.json
    """
    code_version = "0.2.12"

    def __init__(self, configuration_file="resources/config.json"):
        # config.json settings
        self.main_config_file = configuration_file
        self.base_schema_folder = "unknown"
        self.meta_version = "unknown"
        self.schema_directory = "unknown"
        self.json_directory = "unknown"
        self.target = "unknown"
        self.output_directory = "unknown"
        self.metadata_store = "unknown"
        self.mu_log = None
        self.log_config = None
        self.log_directory = None
        self.log_filename = None
        self.log_filename_prefix = None
        self.log_level = None
        self.edc_config = "unknown"
        self.edc_config_data = {}
        self.edc_url = "http://localhost:8888"
        self.edc_secrets = "unknown"
        self.jinja_config = "unknown"
        self.azure_monitor_config = None
        self.azure_monitor_requests = None
        self.instrumentation_key = None
        self.suppress_edc_call = "False"
        self.edc_http_proxy = None
        self.edc_https_proxy = None
        self.edc_auth = None

    def get_config(self):
        """
            get the main configuration settings. default file is resources/config.json
        """
        module = "get_config"
        result = messages.message["undetermined"]

        try:
            with open(self.main_config_file) as config:
                data = json.load(config)
                self.base_schema_folder = data["schema_directory"]
                # self.schema_directory = self.base_schema_folder + self.meta_version + "/"
                self.json_directory = data["json_directory"]
                self.target = data["target"]
                self.output_directory = data["output_directory"]
                self.metadata_store = data["metadata_store"]
                if "edc_config" in data:
                    self.edc_config = data["edc_config"]
                if "edc_secrets" in data:
                    self.edc_secrets = data["edc_secrets"]
                if "jinja_config" in data:
                    self.jinja_config = data["jinja_config"]
                if "suppress_edc_call" in data:
                    if data["suppress_edc_call"] == "True":
                        self.suppress_edc_call = True
                    elif data["suppress_edc_call"] == "False":
                        self.suppress_edc_call = False
                    else:
                        print("Incorrect config value >" + data["suppress_edc_call"]
                              + "< for suppress_edc_call. Must be True or False. Will default to False")
                        self.suppress_edc_call = False
                if "http_proxy" in data:
                    self.http_proxy = data["http_proxy"]
                    if self.http_proxy == "None":
                        self.http_proxy = None
                else:
                    self.http_proxy = None
                if "https_proxy" in data:
                    self.https_proxy = data["https_proxy"]
                    if self.https_proxy == "None":
                        self.https_proxy = None
                else:
                    self.https_proxy = None
                if "log_config" in data:
                    self.log_config = data["log_config"]
                else:
                    self.log_config = "resources/log_config.json"
                self.mu_log = mu_logging.MULogging(self.log_config)
                self.log_directory = self.mu_log.log_setting.log_directory
                self.log_filename = self.mu_log.log_setting.log_filename
                self.log_filename_prefix = self.mu_log.log_setting.log_filename_prefix
                self.log_level = self.mu_log.log_setting.log_level
                self.azure_monitor_config = self.mu_log.log_setting.azure_monitor_config
                self.azure_monitor_requests = self.mu_log.log_setting.azure_monitor_requests
                self.instrumentation_key = self.mu_log.log_setting.instrumentation_key
                self.mu_log.log(self.mu_log.DEBUG, "Configuration file >" + self.main_config_file
                                + "< found and read.", module)

            result = messages.message["ok"]
        except FileNotFoundError:
            print("FATAL:", module, "could find main configuration file >" + self.main_config_file + "<.")
            return messages.message["main_config_not_found"]

        if self.edc_config != "unknown":
            try:
                with open(self.edc_config) as edc:
                    self.edc_config_data = json.load(edc)
                self.mu_log.log(self.mu_log.DEBUG, "EDC Configuration file >" + self.edc_config
                                + "< found and read.", module)
            except FileNotFoundError:
                self.mu_log.log(self.mu_log.FATAL, "Cannot find provided edc_config file >" + self.edc_config + "<."
                                , module)
                return messages.message["edc_config_not_found"]

        if self.edc_secrets == "unknown":
            self.mu_log.log(self.mu_log.DEBUG, "edc_secrets is unknown")
        else:
            edc_secrets_result = self.get_edc_secrets(self.edc_secrets)
            if edc_secrets_result == messages.message["ok"]:
                self.mu_log.log(self.mu_log.DEBUG, "get_edc_secrets returned OK", module)
            else:
                self.mu_log.log(self.mu_log.ERROR, "get_edc_secrets returned: " + edc_secrets_result["code"], module)
                return edc_secrets_result

        if self.azure_monitor_config != "unknown":
            try:
                with open(self.azure_monitor_config) as az_monitor:
                    data = json.load(az_monitor)
                    if "instrumentation_key" in data:
                        self.instrumentation_key = data["instrumentation_key"]
            except FileNotFoundError:
                self.mu_log.log(self.mu_log.FATAL
                                , "Cannot find Azure configuration file, which is needed to get the instrumentation key"
                                , module)
                return messages.message["azure_config_not_found"]

        return result

    def get_edc_proxy(self):

        if self.edc_http_proxy == "None":
            self.edc_http_proxy = None
        if self.edc_https_proxy == "None":
            self.edc_https_proxy = None

        proxies = {
            "http": self.edc_http_proxy,
            "https": self.edc_https_proxy
        }
        return proxies

    def get_edc_secrets(self, edc_secrets="resources/edc.secrets"):
        module = "get_edc_secrets"

        try:
            with open(self.edc_secrets) as edc:
                data = json.load(edc)
                if "edc_url" in data:
                    self.edc_url = data["edc_url"]
                    self.mu_log.log(self.mu_log.INFO, "EDC URL taken from edc secrets file >" + self.edc_secrets
                                    + "<: "
                                    + self.edc_url, module)
                if "edc_auth" in data:
                    self.auth = data["edc_auth"]
                    self.mu_log.log(self.mu_log.INFO, "EDC Authentication taken from edc secrets file.", module)
                else:
                    self.mu_log.log(self.mu_log.WARNING, "No Authentication for EDC found in edc secrets file. "
                                    + "This is OK if the authentication has been set through the environment variable INFA_EDC_AUTH"
                                    ,module)

                if "edc_http_proxy" in data:
                    self.http_proxy = data["edc_http_proxy"]
                    self.mu_log.log(self.mu_log.INFO, "HTTP Proxy for EDC taken from edc secrets file: "
                                    + self.http_proxy, module)
                else:
                    self.mu_log.log(self.mu_log.INFO, "No HTTP Proxy for EDC found in edc secrets file. "
                                    + "This is OK if no proxy is needed or has been set through the environment variable HTTP_PROXY"
                                    , module)
                if "edc_https_proxy" in data:
                    self.https_proxy = data["edc_https_proxy"]
                    self.mu_log.log(self.mu_log.INFO, "HTTPS Proxy for EDC taken from edc secrets file: "
                                    + self.https_proxy, module)
                else:
                    self.mu_log.log(self.mu_log.INFO, "No HTTPS Proxy for EDC found in edc secrets file. "
                                    + "This is OK if no proxy is needed or has been set through the environment variable HTTPS_PROXY"
                                    , module)
            self.mu_log.log(self.mu_log.DEBUG, "EDC secrets file >" + self.edc_secrets + "< found and read.", module)
        except FileNotFoundError:
            self.mu_log.log(self.mu_log.FATAL, "Cannot find provided edc_secrets file >" + self.edc_secrets + "<."
                            , module)
            return messages.message["edc_secrets_not_found"]

        return messages.message["ok"]
