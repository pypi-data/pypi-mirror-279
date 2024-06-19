import logging
import logging.config
import os
import sys
from pathlib import Path

import yaml
from opencensus.ext.azure.log_exporter import AzureLogHandler
from qcaas_common.log_reduct import RedactingFilter

default_logger_format = (
    "[%(levelname)s] %(asctime)s (%(module)s.%(funcName)s:%(lineno)d) - %(message)s"
)


def get_logger_config():
    try:
        logger_config_path = os.environ.get("LOG_CONFIG_PATH", "logger_config.yaml")
        assert Path(logger_config_path).exists()
        with open(logger_config_path, "r") as the_file:
            if the_file is not None:
                return yaml.load(the_file, Loader=yaml.SafeLoader)
    except Exception as e:
        error_msg = "Error while opening logger config" + "\n" + str(e)
        # Logging in stdout amd stderr, since logger not configured yet
        sys.stdout.write(error_msg)


_config_dict = get_logger_config()


def get_logger(module_name):
    """Central method for if/when we need to return a more complicated logging
    instance."""

    if _config_dict is not None:
        logging.config.dictConfig(_config_dict)

    log = logging.getLogger(module_name)
    log.setLevel(logging.getLevelName(os.environ.get("APP_LOG_LEVEL", logging.INFO)))

    # Don't want to duplicate log handling if we've already got one set up.
    if not any(log.handlers):
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logging.Formatter(default_logger_format))
        log.addHandler(stream_handler)

        # This handler sends all messages to an Azure monitor, if set up.
        connection_string = os.environ.get(
            "APPLICATIONINSIGHTS_CONNECTION_STRING", None
        )
        if connection_string is not None:
            azure_logger = AzureLogHandler(
                connection_string=connection_string,
                max_batch_size=1200,
                queue_capacity=16384,
            )
            # Default queue size is 8192, doubled to give sufficient redundancy
            # Max batch size is default 100, set to 1200 to allow up to 1200 messages
            # per second to be cleared
            # consistently
            azure_logger.setFormatter(logging.Formatter(default_logger_format))
            log.addHandler(azure_logger)

        if os.environ.get("LOG_FILTER_ENABLED", "false") == "true":
            try:
                if _config_dict is not None:
                    log.addFilter(
                        RedactingFilter(
                            _config_dict["filters"]["qcaas_filter"]["patterns"]
                        )
                    )
                else:
                    raise KeyError
            except KeyError as e:
                error_msg = "Error while Enabling logger filter" + "\n" + str(e)
                log.error(error_msg)
                # Logging in stdout amd stderr, since logger might not be properly set
                sys.stdout.write(error_msg)
                sys.stderr.write(error_msg)
                raise e

    return log


_logger = get_logger(__name__)

azure_enabled = (
    os.environ.get("APPLICATIONINSIGHTS_CONNECTION_STRING", None) is not None
)
if azure_enabled:
    _logger.info("Azure logging activated.")
else:
    _logger.info("No Azure connection string available.")
