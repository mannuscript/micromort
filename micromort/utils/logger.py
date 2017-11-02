import logging


from micromort.resources.configs.loggerconfig import logger_config

if logger_config["level"] == "INFO":
    logging.basicConfig(level=logging.INFO)
elif logger_config["level"] == "DEBUG":
    logging.basicConfig(level=logging.DEBUG)

logging.Formatter(logger_config["formatter"])
logger = logging.getLogger(__name__)