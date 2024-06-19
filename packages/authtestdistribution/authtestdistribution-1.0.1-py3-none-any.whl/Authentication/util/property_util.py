import configparser
import os
import logging

from Authentication.constants.config_constants import DEFAULT_AUTHENTICATE_CONFIG_PROPERTIES, \
    CUSTOM_AUTHENTICATE_CONFIG_PROPERTIES, FILE_NOT_FOUND_ERR_MESSAGE
from Authentication.exception.authenticate_exception import PropertyNotFoundError

logger = logging.getLogger(__name__)
os.environ['CUSTOM_AUTHENTICATE_CONFIG_PATH'] = CUSTOM_AUTHENTICATE_CONFIG_PROPERTIES
os.environ['DEFAULT_AUTHENTICATE_PROPERTY_FILE'] = DEFAULT_AUTHENTICATE_CONFIG_PROPERTIES

class PropertyUtils:
    config = None

    @staticmethod
    def initialize():
        if PropertyUtils.config is None:
            config = configparser.ConfigParser()
            authenticate_custom_config_file = os.getenv('CUSTOM_AUTHENTICATE_CONFIG_PATH')
            authenticate_default_config_file = os.getenv("DEFAULT_AUTHENTICATE_PROPERTY_FILE")
            property_file = os.path.join(os.path.dirname(__file__), '..', authenticate_default_config_file)
            if authenticate_custom_config_file and os.path.exists(authenticate_custom_config_file):
                config.read(authenticate_custom_config_file)
                logger.info("Reading properties from sdk_application.properties file")
            elif authenticate_default_config_file and os.path.exists(property_file):
                config.read(property_file)
                logger.info("Reading properties from spciq-api-authentication-application.properties file")
            else:
                raise FileNotFoundError(FILE_NOT_FOUND_ERR_MESSAGE)
            PropertyUtils.config = config

    @staticmethod
    def get_property(section, key):
        PropertyUtils.initialize()
        if not PropertyUtils.config.has_section(section):
            raise PropertyNotFoundError(f"Section '{section}' not found in config properties file")
        if not PropertyUtils.config.has_option(section, key):
            raise PropertyNotFoundError(f"Key '{key}' not found in section '{section} of config"
                                        f"properties file'")
        return PropertyUtils.config.get(section, key)
