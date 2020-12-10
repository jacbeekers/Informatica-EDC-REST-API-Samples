from src.metadata_utilities import generic_settings, generic
from src.metadata_utilities import messages
from src.metadata_utilities import mu_logging
from src.informatica import bulkResourceDelete


def get_settings(name="tests/resources/config.json"):
    settings = generic_settings.GenericSettings(name)
    settings.get_config()
    mu_log = mu_logging.MULogging(settings.log_config)
    generic_ref = generic.Generic(settings=settings, mu_log_ref=mu_log)
    return settings, mu_log, generic_ref


def test_bulk_resource_delete():
    name = "dummy"
    bulkResourceDelete.main()

