import logging.config
from pythonjsonlogger import jsonlogger

def setup_logging():
    # Load the basic logging configuration from the config file
    logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

    # Create a JSON formatter
    json_formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(funcName)s %(lineno)d %(message)s'
    )

    # Apply the JSON formatter to all handlers of all loggers
    for logger_name in logging.root.manager.loggerDict:
        logger = logging.getLogger(logger_name)
        for handler in logger.handlers:
            handler.setFormatter(json_formatter)
