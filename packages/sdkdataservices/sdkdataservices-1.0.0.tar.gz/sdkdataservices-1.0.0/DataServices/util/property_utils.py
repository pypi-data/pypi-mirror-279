import configparser
import os
import logging
os.environ['CUSTOM_CONFIG_PATH'] = 'config/custom-config.properties'
os.environ['DEFAULT_PROPERTY_FILE'] = 'config/spciq-api-dataservices-application.properties'
logger = logging.getLogger(__name__)
class PropertyUtils:
    config = None

    @staticmethod
    def load_config():
        try:
            if PropertyUtils.config is None:
                config = configparser.ConfigParser()
                custom_config_file = os.getenv('CUSTOM_CONFIG_PATH')
                default_config_file = os.getenv("DEFAULT_PROPERTY_FILE")
                property_file = os.path.join(os.path.dirname(__file__), '..', default_config_file)
                if custom_config_file and os.path.exists(custom_config_file):
                    config.read(custom_config_file)
                    logger.info("Reading properties from custom properties file")
                elif default_config_file and os.path.exists(property_file):
                    config.read(property_file)
                    logger.info("Reading properties from default properties file")
                else:
                    raise FileNotFoundError(f"default configuration file not found: {property_file}")
                PropertyUtils.config = config
        except FileNotFoundError as e:
            print(f"Configuration file not found: {e}")

    @staticmethod
    def get_property(section, key):
        PropertyUtils.load_config()
        return PropertyUtils.config.get(section, key, fallback=None)

    @staticmethod
    def check_version(url, versions):
        return any(version in url.strip() for version in versions)


